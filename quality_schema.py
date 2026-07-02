from typing import Optional
from pydantic import BaseModel


class QualityIssueResolveRequest(BaseModel):
    resolved_by: Optional[str] = None
    resolution_comment: Optional[str] = None
