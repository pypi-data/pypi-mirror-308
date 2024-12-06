import asyncio
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Set, Tuple, TypeVar

import aiohttp
import requests
import tiktoken
from tqdm import tqdm
from functools import partial

from bespokelabs.curator.dataset import Dataset
from bespokelabs.curator.request_processor.base_request_processor import (
    BaseRequestProcessor,
    GenericRequest,
    GenericResponse,
)
from bespokelabs.curator.prompter.prompter import PromptFormatter

T = TypeVar("T")
logger = logging.getLogger(__name__)


class OpenAIOnlineRequestProcessor(BaseRequestProcessor):
    def __init__(
        self,
        batch_size: Optional[int] = None,
        model: str = "gpt-4o-mini",
        api_key: str = os.getenv("OPENAI_API_KEY"),
        url: str = "https://api.openai.com/v1/chat/completions",
    ):
        super().__init__(batch_size)
        self.model: str = model
        self.url: str = url
        self.api_key: str = api_key

    def get_rate_limits(self) -> dict:
        """
        Function to get rate limits for a given annotator. Makes a single request to openAI API
        and gets the rate limits from the response headers. These rate limits vary per model
        and are determined by your organization's usage tier. View the following:
        https://platform.openai.com/docs/guides/rate-limits/usage-tiers
        https://platform.openai.com/settings/organization/limits

        Args:
            model (str): The model for which to get the rate limits.
            request_url (str): The request URL for which to get the rate limits.

        Returns:
            tuple[int, int]: A tuple containing the maximum number of requests and tokens per minute.
        """
        # Send a dummy request to get rate limit information
        response = requests.post(
            self.url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": []},
        )

        rpm = int(response.headers.get("x-ratelimit-limit-requests", 0))
        tpm = int(response.headers.get("x-ratelimit-limit-tokens", 0))

        if not rpm or not tpm:
            logger.warning(
                "Failed to get rate limits from OpenAI API, using default values"
            )
            rpm = 30_000
            tpm = 150_000_000

        logger.info(f"Automatically set max_requests_per_minute to {rpm}")
        logger.info(f"Automatically set max_tokens_per_minute to {tpm}")

        rate_limits = {
            "max_requests_per_minute": rpm,
            "max_tokens_per_minute": tpm,
        }

        return rate_limits

    def create_api_specific_request(self, generic_request: GenericRequest) -> dict:
        """
        Creates a API-specific request body from a generic request body.

        Using the api_parallel_processor, we can store whatever we want in the metadata. We will store both the row and the index.
        This is so we can later construct the new dataset row.

        Returns:
            dict: API specific request body
        """
        if generic_request.response_format:
            request = {
                "model": generic_request.model,
                "messages": generic_request.messages,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        # TODO(ryan): not sure if we should use strict: True or have name: be something else.
                        "name": "output_schema",
                        "schema": generic_request.response_format.model_json_schema(),
                    },
                },
                "metadata": {
                    "request_idx": generic_request.row_idx,
                    "sample": generic_request.row,
                },
            }
        else:
            request = {
                "model": generic_request.model,
                "messages": generic_request.messages,
                "metadata": {
                    "request_idx": generic_request.row_idx,
                    "sample": generic_request.row,
                },
            }

        return request

    def get_generic_response(
        self, response: Dict, prompt_formatter: PromptFormatter
    ) -> GenericResponse:
        """
        Parses a API-specific response into a generic response body.
        Does error handling on the response.
        If there is an error, return None.

        IMPORTANT: In the generic response body you need to provide either the original dataset row OR the index of the row in the original dataset.

        Args:
            response: API-specific response

        Returns:
            dict: Generic response body with an extra field "metadata" which contains the original dataset row or the index of the row in the original dataset
        """
        content = response["response"]["choices"][0]["message"]["content"]
        if prompt_formatter.response_format:
            content = json.loads(content)

        return GenericResponse(
            response=content,
            row=response["metadata"][
                "sample"
            ],  # Or can do dataset[response["metadata"]["request_idx"]]
            row_idx=response["metadata"]["request_idx"],
        )

    def run(
        self,
        dataset: Optional[Dataset],
        working_dir: str,
        prompt_formatter: PromptFormatter,
    ) -> Dataset:
        """
        Uses the API to completing the specific map by calling the LLM.

        Args:
            dataset (Dataset): Dataset that is being mapped over
            working_dir (str): Working directory to save files (requests.jsonl, responses.jsonl, dataset.arrow)

        Returns:
            Dataset: Completed dataset
        """
        requests_files = self.create_request_files(
            dataset, working_dir, prompt_formatter
        )
        responses_files = [
            f"{working_dir}/responses_{i}.jsonl" for i in range(len(requests_files))
        ]

        rate_limits = self.get_rate_limits()
        rpm = rate_limits["max_requests_per_minute"]
        tpm = rate_limits["max_tokens_per_minute"]

        token_encoding_name = get_token_encoding_name(prompt_formatter.model_name)

        # NOTE(Ryan): If you wanted to do this on batches, you could run a for loop here about request_files. Although I don't recommend it because you are waiting for straggler requests to finish for each batch.
        # NOTE(Ryan): And if you wanted to do batches in parallel, you would have to divide rpm and tpm by the number of parallel batches.
        # TODO(Ryan): Can we abstract retries from process_api_requests_from_file so you can use it even if you use liteLLM.
        for requests_file, responses_file in zip(requests_files, responses_files):
            asyncio.run(
                self.process_api_requests_from_file(
                    requests_filepath=requests_file,
                    save_filepath=responses_file,
                    request_url=self.url,
                    max_requests_per_minute=rpm,
                    max_tokens_per_minute=tpm,
                    token_encoding_name=token_encoding_name,
                    max_attempts=5,
                    resume=True,  # detects existing jobs and resume from there
                    prompt_formatter=prompt_formatter,
                )
            )

        dataset = self.create_dataset_files(dataset, working_dir, prompt_formatter)
        return dataset

    async def process_api_requests_from_file(
        self,
        requests_filepath: str,
        save_filepath: str,
        request_url: str,
        max_requests_per_minute: float,
        max_tokens_per_minute: float,
        token_encoding_name: str,
        max_attempts: int,
        resume: bool,
        prompt_formatter: PromptFormatter,
        resume_no_retry: bool = False,
    ) -> None:
        """Processes API requests in parallel, throttling to stay under rate limits."""
        # constants
        seconds_to_pause_after_rate_limit_error = 15
        seconds_to_sleep_each_loop = (
            0.001  # 1 ms limits max throughput to 1,000 requests per second
        )

        # infer API endpoint and construct request header
        api_endpoint = api_endpoint_from_url(self.url)
        request_header = {"Authorization": f"Bearer {self.api_key}"}
        # use api-key header for Azure deployments
        if "/deployments" in self.url:
            request_header = {"api-key": f"{self.api_key}"}

        # initialize trackers
        queue_of_requests_to_retry = asyncio.Queue()
        task_id_generator = (
            task_id_generator_function()
        )  # generates integer IDs of 0, 1, 2, ...
        status_tracker = (
            StatusTracker()
        )  # single instance to track a collection of variables
        next_request = None  # variable to hold the next request to call

        # initialize available capacity counts
        available_request_capacity = max_requests_per_minute
        available_token_capacity = max_tokens_per_minute
        last_update_time = time.time()

        # initialize flags
        file_not_finished = True  # after file is empty, we'll skip reading it
        logger.debug(f"Initialization complete.")

        completed_request_ids: Set[int] = set()
        if os.path.exists(save_filepath):
            if resume:
                # save all successfully completed requests to a temporary file, then overwrite the original file with the temporary file
                logger.debug(f"Resuming progress from existing file: {save_filepath}")
                logger.debug(
                    f"Removing all failed requests from {save_filepath} so they can be retried"
                )
                temp_filepath = f"{save_filepath}.temp"
                num_previously_failed_requests = 0
                with open(save_filepath, "r") as input_file, open(
                    temp_filepath, "w"
                ) as output_file:
                    for line in input_file:
                        response = GenericResponse.model_validate_json(line)
                        if response.errors:
                            # this means that the request failed and we have a list of errors
                            logger.debug(
                                f"Request {response.row_idx} previously failed due to errors: {response.errors}, removing from output and will retry"
                            )
                            num_previously_failed_requests += 1
                        else:
                            completed_request_ids.add(response.row_idx)
                            output_file.write(line)
                logger.info(
                    f"Found {len(completed_request_ids)} completed requests and {num_previously_failed_requests} previously failed requests"
                )
                logger.info(
                    "Failed requests and remaining requests will now be processed."
                )
                os.replace(temp_filepath, save_filepath)
            elif resume_no_retry:
                logger.warning(
                    f"Resuming progress from existing file: {save_filepath}, without retrying failed requests"
                )
                num_previously_failed_requests = 0
                with open(save_filepath, "r") as input_file, open(
                    temp_filepath, "w"
                ) as output_file:
                    for line in tqdm(input_file, desc="Processing existing requests"):
                        data = json.loads(line)
                        if isinstance(data[1], list):
                            # this means that the request failed and we have a list of errors
                            logger.debug(
                                f"Request {data[2].get('request_idx')} previously failed due to errors: {data[1]}, will NOT retry"
                            )
                            num_previously_failed_requests += 1
                        completed_request_ids.add(data[2].get("request_idx"))
                logger.info(
                    f"Found {len(completed_request_ids)} total requests and {num_previously_failed_requests} previously failed requests"
                )
                logger.info("Remaining requests will now be processed.")
            else:
                user_input = input(
                    f"File {save_filepath} already exists.\nTo resume if there are remaining requests without responses, run with --resume flag.\nOverwrite? (Y/n): "
                )
                if user_input.lower() != "y" and user_input.lower() != "":
                    logger.info("Aborting operation.")
                    return

        # initialize file reading
        with open(requests_filepath) as file:
            # `requests` will provide requests one at a time
            requests = file.__iter__()
            logger.debug(f"File opened. Entering main loop")

            # Count total number of requests
            total_requests = sum(1 for _ in open(requests_filepath))
            if total_requests == len(completed_request_ids):
                logger.debug(
                    "All requests have already been completed so will just reuse cache."
                )
                return

            # Create progress bar
            pbar = tqdm(
                total=total_requests, desc="Processing parallel requests to OpenAI"
            )

            connector = aiohttp.TCPConnector(limit=10 * max_requests_per_minute)
            async with aiohttp.ClientSession(
                connector=connector
            ) as session:  # Initialize ClientSession here
                while True:
                    # get next request (if one is not already waiting for capacity)
                    if next_request is None:
                        if not queue_of_requests_to_retry.empty():
                            next_request = queue_of_requests_to_retry.get_nowait()
                            logger.debug(
                                f"Retrying request {next_request.task_id}: {next_request}"
                            )
                        elif file_not_finished:
                            try:
                                # get new request
                                request_json = json.loads(next(requests))
                                request_idx = request_json["metadata"]["request_idx"]
                                if resume and request_idx in completed_request_ids:
                                    logger.debug(
                                        f"Skipping already completed request {request_idx}"
                                    )
                                    status_tracker.num_tasks_already_completed += 1
                                    continue
                                next_request = APIRequest(
                                    task_id=next(task_id_generator),
                                    request_json=request_json,
                                    token_consumption=num_tokens_consumed_from_request(
                                        request_json, api_endpoint, token_encoding_name
                                    ),
                                    attempts_left=max_attempts,
                                    metadata=request_json.pop("metadata", None),
                                )
                                status_tracker.num_tasks_started += 1
                                status_tracker.num_tasks_in_progress += 1
                                logger.debug(
                                    f"Reading request {next_request.task_id}: {next_request}"
                                )
                            except StopIteration:
                                # if file runs out, set flag to stop reading it
                                logger.debug("Read file exhausted")
                                file_not_finished = False

                    # update available capacity
                    current_time = time.time()
                    seconds_since_update = current_time - last_update_time
                    available_request_capacity = min(
                        available_request_capacity
                        + max_requests_per_minute * seconds_since_update / 60.0,
                        max_requests_per_minute,
                    )
                    available_token_capacity = min(
                        available_token_capacity
                        + max_tokens_per_minute * seconds_since_update / 60.0,
                        max_tokens_per_minute,
                    )
                    last_update_time = current_time

                    # if enough capacity available, call API
                    if next_request:
                        next_request_tokens = next_request.token_consumption
                        if (
                            available_request_capacity >= 1
                            and available_token_capacity >= next_request_tokens
                        ):
                            # update counters
                            available_request_capacity -= 1
                            available_token_capacity -= next_request_tokens
                            next_request.attempts_left -= 1

                            # call API
                            asyncio.create_task(
                                next_request.call_api(
                                    session=session,
                                    request_url=request_url,
                                    request_header=request_header,
                                    retry_queue=queue_of_requests_to_retry,
                                    save_filepath=save_filepath,
                                    status_tracker=status_tracker,
                                    get_generic_response=partial(
                                        self.get_generic_response,
                                        prompt_formatter=prompt_formatter,
                                    ),
                                )
                            )
                            next_request = None  # reset next_request to empty
                        else:
                            logger.debug(
                                f"Not Enough Capacity: Request tokens: {next_request_tokens}, Available request capacity: {available_request_capacity}, Available token capacity: {available_token_capacity}"
                            )

                    # Update progress bar when a task is completed
                    total_completed = (
                        status_tracker.num_tasks_succeeded
                        + status_tracker.num_tasks_failed
                        + status_tracker.num_tasks_already_completed
                    )
                    if total_completed > pbar.n:
                        pbar.update(total_completed - pbar.n)

                    # if all tasks are finished, break
                    if status_tracker.num_tasks_in_progress == 0:
                        break

                    # main loop sleeps briefly so concurrent tasks can run
                    await asyncio.sleep(seconds_to_sleep_each_loop)

                    # if a rate limit error was hit recently, pause to cool down
                    seconds_since_rate_limit_error = (
                        time.time() - status_tracker.time_of_last_rate_limit_error
                    )
                    if (
                        seconds_since_rate_limit_error
                        < seconds_to_pause_after_rate_limit_error
                    ):
                        remaining_seconds_to_pause = (
                            seconds_to_pause_after_rate_limit_error
                            - seconds_since_rate_limit_error
                        )
                        await asyncio.sleep(remaining_seconds_to_pause)
                        # ^e.g., if pause is 15 seconds and final limit was hit 5 seconds ago
                        logger.warn(
                            f"Pausing to cool down until {time.ctime(status_tracker.time_of_last_rate_limit_error + seconds_to_pause_after_rate_limit_error)}"
                        )

            # Close the progress bar
            pbar.close()

            # after finishing, log final status
            logger.info(
                f"""Parallel processing complete. Results saved to {save_filepath}"""
            )

            logger.info(f"Status tracker: {status_tracker}")

            if status_tracker.num_tasks_failed > 0:
                logger.warning(
                    f"{status_tracker.num_tasks_failed} / {status_tracker.num_tasks_started} requests failed. Errors logged to {save_filepath}."
                )
            if status_tracker.num_rate_limit_errors > 0:
                logger.warning(
                    f"{status_tracker.num_rate_limit_errors} rate limit errors received. Consider running at a lower rate."
                )


@dataclass
class StatusTracker:
    """Stores metadata about the script's progress. Only one instance is created."""

    num_tasks_already_completed: int = 0
    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0  # script ends when this reaches 0
    num_tasks_succeeded: int = 0
    num_tasks_failed: int = 0
    num_rate_limit_errors: int = 0
    num_api_errors: int = 0  # excluding rate limit errors, counted above
    num_other_errors: int = 0
    time_of_last_rate_limit_error: int = 0  # used to cool off after hitting rate limits


@dataclass
class APIRequest:
    """Stores an API request's inputs, outputs, and other metadata. Contains a method to make an API call."""

    task_id: int
    request_json: dict
    token_consumption: int
    attempts_left: int
    metadata: dict
    result: list = field(default_factory=list)

    async def call_api(
        self,
        session: aiohttp.ClientSession,
        request_url: str,
        request_header: dict,
        retry_queue: asyncio.Queue,
        save_filepath: str,
        status_tracker: StatusTracker,
        get_generic_response: Callable[[list], dict],
    ) -> None:
        """Calls the OpenAI API and saves results."""
        logger.debug(f"Starting request #{self.task_id}")
        error = None
        try:
            async with session.post(
                url=request_url, headers=request_header, json=self.request_json
            ) as response:
                response = await response.json()
            if "error" in response:
                logger.warning(
                    f"Request {self.task_id} failed with error {response['error']}"
                )
                status_tracker.num_api_errors += 1
                error = response
                if "rate limit" in response["error"].get("message", "").lower():
                    status_tracker.time_of_last_rate_limit_error = time.time()
                    status_tracker.num_rate_limit_errors += 1
                    status_tracker.num_api_errors -= (
                        1  # rate limit errors are counted separately
                    )

        except (
            Exception
        ) as e:  # catching naked exceptions is bad practice, but in this case we'll log & save them
            logger.warning(
                f"Request {self.task_id} failed with Exception {e}, attempts left {self.attempts_left}"
            )
            status_tracker.num_other_errors += 1
            error = e
        if error:
            self.result.append(error)
            if self.attempts_left:
                retry_queue.put_nowait(self)
            else:
                logger.error(
                    f"Request {self.request_json} failed after all attempts. Saving errors: {self.result}"
                )
                data = GenericResponse(
                    request=self.request_json,
                    errors=[str(e) for e in self.result],
                    row=self.metadata["sample"],
                    row_idx=self.metadata["request_idx"],
                )
                append_generic_response(data, save_filepath)
                status_tracker.num_tasks_in_progress -= 1
                status_tracker.num_tasks_failed += 1
        else:
            data = get_generic_response(
                {"response": response, "metadata": self.metadata}
            )
            data.raw_response = response
            data.request = self.request_json
            append_generic_response(data, save_filepath)
            status_tracker.num_tasks_in_progress -= 1
            status_tracker.num_tasks_succeeded += 1
            logger.debug(f"Request {self.task_id} saved to {save_filepath}")


def get_token_encoding_name(model: str) -> str:
    """Get the token encoding name for a given model."""
    if "gpt" in model:
        return tiktoken.encoding_for_model(model).name
    else:
        logger.warning(
            f'Token encoding name for model "{model}" not implemented, using cl100k_base for token counting'
        )
        return "cl100k_base"


def get_rate_limits(model: str, request_url: str, api_key: str) -> Tuple[int, int]:
    """
    Function to get rate limits for a given annotator. Makes a single request to openAI API
    and gets the rate limits from the response headers. These rate limits vary per model
    and are determined by your organization's usage tier. View the following:
    https://platform.openai.com/docs/guides/rate-limits/usage-tiers
    https://platform.openai.com/settings/organization/limits

    Args:
        model (str): The model for which to get the rate limits.
        request_url (str): The request URL for which to get the rate limits.

    Returns:
        Tuple[int, int]: The maximum number of requests and tokens per minute.
    """
    if "api.openai.com" in request_url:
        # Send a dummy request to get rate limit information
        response = requests.post(
            request_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": model, "messages": []},
        )
        # Extract rate limit information from headers
        max_requests = int(response.headers.get("x-ratelimit-limit-requests", 30_000))
        max_tokens = int(response.headers.get("x-ratelimit-limit-tokens", 150_000_000))
    elif "api.sambanova.ai" in request_url:
        # Send a dummy request to get rate limit information
        max_requests = 50
        max_tokens = 100_000_000
    else:
        raise NotImplementedError(
            f'Rate limits for API endpoint "{request_url}" not implemented'
        )

    return max_requests, max_tokens


def get_api_key(request_url: str) -> str:
    """Get the API key for a given request URL."""
    if "api.openai.com" in request_url:
        return os.getenv("OPENAI_API_KEY")
    elif "api.sambanova.ai" in request_url:
        return os.getenv("SAMBANOVA_API_KEY")
    else:
        raise NotImplementedError(
            f'Default API key environment variable for API endpoint "{request_url}" not implemented'
        )


def api_endpoint_from_url(request_url: str) -> str:
    """Extract the API endpoint from the request URL.
    This is used to determine the number of tokens consumed by the request.
    """

    # OpenAI API
    match = re.search("^https://[^/]+/v\\d+/(.+)$", request_url)
    if match:
        return match[1]

    # for Azure OpenAI deployment urls
    match = re.search(
        r"^https://[^/]+/openai/deployments/[^/]+/(.+?)(\?|$)", request_url
    )
    if match:
        return match[1]

    # Catch all for other API endpoints using OpenAI OpenAPI format
    if "chat/completions" in request_url:
        return "chat/completions"
    elif "completions" in request_url:
        return "completions"
    else:
        raise NotImplementedError(
            f'API endpoint "{request_url}" not implemented in this script'
        )


def append_generic_response(data: GenericResponse, filename: str) -> None:
    """Append a json payload to the end of a jsonl file."""
    json_string = json.dumps(data.model_dump())
    with open(filename, "a") as f:
        f.write(json_string + "\n")


def num_tokens_consumed_from_request(
    request_json: dict,
    api_endpoint: str,
    token_encoding_name: str,
):
    """Count the number of tokens in the request. Only supports completion and embedding requests."""
    encoding = tiktoken.get_encoding(token_encoding_name)
    # if completions request, tokens = prompt + n * max_tokens
    if api_endpoint.endswith("completions"):
        max_tokens = request_json.get("max_tokens", 15)
        n = request_json.get("n", 1)
        completion_tokens = n * max_tokens

        # chat completions
        if api_endpoint.startswith("chat/"):
            num_tokens = 0
            for message in request_json["messages"]:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens -= 1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens + completion_tokens
        # normal completions
        else:
            prompt = request_json["prompt"]
            if isinstance(prompt, str):  # single prompt
                prompt_tokens = len(encoding.encode(prompt))
                num_tokens = prompt_tokens + completion_tokens
                return num_tokens
            elif isinstance(prompt, list):  # multiple prompts
                prompt_tokens = sum([len(encoding.encode(p)) for p in prompt])
                num_tokens = prompt_tokens + completion_tokens * len(prompt)
                return num_tokens
            else:
                raise TypeError(
                    'Expecting either string or list of strings for "prompt" field in completion request'
                )
    # if embeddings request, tokens = input tokens
    elif api_endpoint == "embeddings":
        input = request_json["input"]
        if isinstance(input, str):  # single input
            num_tokens = len(encoding.encode(input))
            return num_tokens
        elif isinstance(input, list):  # multiple inputs
            num_tokens = sum([len(encoding.encode(i)) for i in input])
            return num_tokens
        else:
            raise TypeError(
                'Expecting either string or list of strings for "inputs" field in embedding request'
            )
    # more logic needed to support other API calls (e.g., edits, inserts, DALL-E)
    else:
        raise NotImplementedError(
            f'API endpoint "{api_endpoint}" not implemented in this script'
        )


def task_id_generator_function():
    """Generate integers 0, 1, 2, and so on."""
    task_id = 0
    while True:
        yield task_id
        task_id += 1
