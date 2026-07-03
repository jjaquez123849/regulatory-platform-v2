from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user, require_admin
from app.core.database import get_db
from app.models.security import User
from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse
)
from app.services.auth_service import (
    create_user,
    list_users,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        return login_user(
            db=db,
            username=payload.username,
            password=payload.password
        )
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))


@router.get("/me", response_model=UserResponse)
def read_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/users", response_model=UserResponse)
def create_new_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        return create_user(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/users", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return list_users(db)
