from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.security import User


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="No autenticado.")

    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")

    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Token inválido.")

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no válido.")

    return user


def require_roles(*allowed_roles: str):
    def checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.is_superuser:
            return current_user

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="No tiene permisos para realizar esta acción."
            )

        return current_user

    return checker


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.is_superuser or current_user.role == "admin":
        return current_user

    raise HTTPException(
        status_code=403,
        detail="Se requiere rol administrador."
    )
