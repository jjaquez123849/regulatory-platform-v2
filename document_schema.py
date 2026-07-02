from typing import Optional
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    record_id: Optional[int] = None
    document_type_id: Optional[int] = None
    original_filename: str
    stored_filename: str
    file_extension: Optional[str] = None
    mime_type: Optional[str] = None
    direction: str
    processing_status: str
    ai_summary: Optional[str] = None
    ai_confidence: Optional[str] = None
    uploaded_by: Optional[str] = None

    class Config:
        from_attributes = True
