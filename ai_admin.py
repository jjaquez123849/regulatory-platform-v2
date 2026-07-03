from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_schema import (
    AIConfigurationCreate,
    AIConfigurationResponse
)
from app.services.ai_config_service import (
    create_ai_configuration,
    list_ai_configurations
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin - AI"]
)


@router.post("/ai-configurations", response_model=AIConfigurationResponse)
def create_new_ai_configuration(
    payload: AIConfigurationCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_ai_configuration(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/ai-configurations", response_model=list[AIConfigurationResponse])
def read_ai_configurations(
    process_id: int | None = Query(None),
    document_type_id: int | None = Query(None),
    purpose: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return list_ai_configurations(
        db=db,
        process_id=process_id,
        document_type_id=document_type_id,
        purpose=purpose
    )
