from typing import Optional
from pydantic import BaseModel


class LocalAIModelCreate(BaseModel):
    name: str
    engine_type: str = "rule_based"
    model_path: Optional[str] = None
    model_name: Optional[str] = None
    context_size: int = 4096
    temperature: str = "0.2"
    is_default: bool = False
    is_active: bool = True
    notes: Optional[str] = None


class LocalAIModelResponse(BaseModel):
    id: int
    name: str
    engine_type: str
    model_path: Optional[str] = None
    model_name: Optional[str] = None
    context_size: int
    temperature: str
    is_default: bool
    is_active: bool
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class LocalAITestRequest(BaseModel):
    prompt: str
    model_id: Optional[int] = None


class LocalAITestResponse(BaseModel):
    engine_type: str
    available: bool
    response: str
