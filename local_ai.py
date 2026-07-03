from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.engines.local_ai.local_ai_orchestrator import LocalAIOrchestrator
from app.models.security import User
from app.schemas.local_ai_schema import (
    LocalAIModelCreate,
    LocalAIModelResponse,
    LocalAITestRequest,
    LocalAITestResponse,
)
from app.services.local_ai_config_service import (
    create_local_ai_model,
    list_local_ai_models,
)


router = APIRouter(
    prefix="/local-ai",
    tags=["Local AI"],
)


@router.post("/models", response_model=LocalAIModelResponse)
def create_model(
    payload: LocalAIModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_local_ai_model(db, payload.model_dump())


@router.get("/models", response_model=list[LocalAIModelResponse])
def read_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_local_ai_models(db)


@router.post("/test", response_model=LocalAITestResponse)
def test_local_ai(
    payload: LocalAITestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orchestrator = LocalAIOrchestrator(db)

    return orchestrator.test_prompt(
        prompt=payload.prompt,
        model_id=payload.model_id,
    )
