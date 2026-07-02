from typing import Optional
from pydantic import BaseModel


class ExtractionResultUpdate(BaseModel):
    normalized_value: Optional[str] = None
    status: Optional[str] = None
    reviewed_by: Optional[str] = None
