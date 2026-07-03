from typing import Any, Dict
from pydantic import BaseModel


class AutomationRunRequest(BaseModel):
    process_id: int
    trigger_event: str
    context: Dict[str, Any] = {}
