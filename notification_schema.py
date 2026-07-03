from typing import Optional
from pydantic import BaseModel


class NotificationUpdate(BaseModel):
    status: Optional[str] = None
