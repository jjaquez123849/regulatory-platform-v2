from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.schemas.log_schema import LogValuesUpdateRequest
from app.services.log_edit_service import update_log_values


router = APIRouter(
    prefix="/log-edit",
    tags=["Log Edit"],
)


@router.put("/records/{record_id}/values")
def update_record_log_values(
    record_id: int,
    payload: LogValuesUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_log_values(
            db=db,
            record_id=record_id,
            values=[item.model_dump() for item in payload.values],
            updated_by=current_user.username,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
