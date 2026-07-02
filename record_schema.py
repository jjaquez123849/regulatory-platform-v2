from typing import Any, Dict, Optional, List
from pydantic import BaseModel


class RecordCreate(BaseModel):
    process_id: int
    title: Optional[str] = None
    summary: Optional[str] = None
    source_channel: Optional[str] = None
    created_by: Optional[str] = None
    values: Dict[str, Any] = {}


class RecordUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    source_channel: Optional[str] = None
    is_complete: Optional[bool] = None
    has_pending_items: Optional[bool] = None
    values: Optional[Dict[str, Any]] = None


class RecordValueItem(BaseModel):
    field_id: int
    field_name: str
    field_label: str
    field_type: str
    value: Optional[Any] = None


class RecordResponse(BaseModel):
    id: int
    process_id: int
    current_state_id: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    source_channel: Optional[str] = None
    is_complete: bool
    has_pending_items: bool
    values: List[RecordValueItem] = []
