from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.services.log_intelligence_service import get_log_completion_status


router = APIRouter(
    prefix="/log-intelligence",
    tags=["Log Intelligence"],
)


@router.get("/records/{record_id}/completion")
def read_log_completion(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_log_completion_status(db=db, record_id=record_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
