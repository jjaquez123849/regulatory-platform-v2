from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)
from app.models.security import User


def create_user(db: Session, data: dict) -> User:
    existing = (
        db.query(User)
        .filter(User.username == data["username"])
        .first()
    )

    if existing:
        raise ValueError("Ya existe un usuario con ese username.")

    user = User(
        username=data["username"],
        full_name=data.get("full_name"),
        email=data.get("email"),
        password_hash=hash_password(data["password"]),
        role=data.get("role", "analyst"),
        area=data.get("area"),
        is_active=data.get("is_active", True),
        is_superuser=data.get("is_superuser", False),
        created_at=datetime.utcnow()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    username: str,
    password: str
) -> User | None:
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    user.last_login_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, username: str, password: str) -> dict:
    user = authenticate_user(
        db=db,
        username=username,
        password=password
    )

    if not user:
        raise ValueError("Usuario o contraseña inválidos.")

    token = create_access_token(
        {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role,
            "area": user.area,
            "is_superuser": user.is_superuser
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def list_users(db: Session) -> list[User]:
    return (
        db.query(User)
        .order_by(User.username.asc())
        .all()
    )
