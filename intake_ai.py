from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.engines.ai.ai_engine_factory import get_ai_engine
from app.models.security import User


router = APIRouter(
    prefix="/intake-ai",
    tags=["Intake AI"],
)


class IntakeAnalyzeTextRequest(BaseModel):
    text: str


@router.post("/analyze-text")
def analyze_text(
    payload: IntakeAnalyzeTextRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    engine = get_ai_engine(db=db)
    result = engine.understand_regulatory_request(payload.text)

    return result.to_dict()
