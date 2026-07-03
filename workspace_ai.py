from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.services.workspace_ai_service import run_workspace_ai_analysis


router = APIRouter(
    prefix="/workspace-ai",
    tags=["Workspace AI"],
)


@router.post("/records/{record_id}/analyze")
def analyze_workspace(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return run_workspace_ai_analysis(
            db=db,
            record_id=record_id,
            current_user=current_user,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
