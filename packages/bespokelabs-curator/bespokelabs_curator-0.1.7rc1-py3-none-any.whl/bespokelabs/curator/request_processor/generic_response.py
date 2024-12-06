from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class GenericResponse(BaseModel):
    response: Optional[Dict[str, Any]] | str = None
    request: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    row: Optional[Dict[str, Any]] = None
    row_idx: int
    raw_response: Optional[Dict[str, Any]] = None  # Note: this is just backlog, not use it directly
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# create time
# end time

# validation
