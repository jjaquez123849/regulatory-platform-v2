from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services.comment_service import create_comment, list_comments


router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post("/", response_model=CommentResponse)
def create_new_comment(
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        data = payload.model_dump()
        data["created_by"] = current_user.username

        return create_comment(db, data)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/records/{record_id}", response_model=list[CommentResponse])
def read_record_comments(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_comments(db, record_id)
