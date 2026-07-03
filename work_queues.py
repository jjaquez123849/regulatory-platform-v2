from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.services.work_queue_service import get_work_queues


router = APIRouter(
    prefix="/work-queues",
    tags=["Work Queues"],
)


@router.get("/")
def read_work_queues(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_work_queues(
        db=db,
        current_user=current_user,
    )
