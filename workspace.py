from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.services.workspace_service import get_record_workspace


router = APIRouter(
    prefix="/workspace",
    tags=["Workspace"],
)


@router.get("/records/{record_id}")
def read_record_workspace(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_record_workspace(
            db=db,
            record_id=record_id,
            current_user=current_user,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
