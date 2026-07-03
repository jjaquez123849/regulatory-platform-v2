from typing import Optional
from pydantic import BaseModel


class CommentCreate(BaseModel):
    record_id: int
    comment_text: str
    comment_type: str = "general"
    created_by: Optional[str] = None


class CommentResponse(BaseModel):
    id: int
    record_id: int
    comment_text: str
    comment_type: str
    created_by: Optional[str] = None

    class Config:
        from_attributes = True
