from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.rir.rir_validator import validate_rir


router = APIRouter(
    prefix="/rir",
    tags=["RIR"],
)


@router.post("/validate")
def validate_rir_payload(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return validate_rir(payload)
