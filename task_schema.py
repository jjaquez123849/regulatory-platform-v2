from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TaskCreate(BaseModel):
    record_id: int
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_area: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    created_by: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_area: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_by: Optional[str] = None
