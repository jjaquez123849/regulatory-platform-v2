from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.security import User
from app.services.auth_service import create_user


router = APIRouter(
    prefix="/security-seed",
    tags=["Security Seed"]
)


@router.post("/admin")
def create_initial_admin(
    db: Session = Depends(get_db)
):
    existing = (
        db.query(User)
        .filter(User.username == "admin")
        .first()
    )

    if existing:
        return {
            "status": "exists",
            "message": "El usuario admin ya existe.",
            "username": existing.username
        }

    user = create_user(
        db=db,
        data={
            "username": "admin",
            "password": "admin123",
            "full_name": "Administrador",
            "email": None,
            "role": "admin",
            "area": "Administración",
            "is_active": True,
            "is_superuser": True
        }
    )

    return {
        "status": "created",
        "message": "Usuario admin creado.",
        "username": user.username,
        "temporary_password": "admin123"
    }
