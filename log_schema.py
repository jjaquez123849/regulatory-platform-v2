from typing import Any
from pydantic import BaseModel


class LogValueUpdate(BaseModel):
    field_id: int
    value: Any = None


class LogValuesUpdateRequest(BaseModel):
    values: list[LogValueUpdate]
    updated_by: str | None = None
