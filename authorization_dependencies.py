from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.domains.iam.services.authorization_service import AuthorizationService
from app.models.security import User


def require_permission(permission_code: str):
    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        authorization = AuthorizationService(db)

        if not authorization.can(current_user, permission_code):
            raise HTTPException(
                status_code=403,
                detail=f"No tiene permiso requerido: {permission_code}",
            )

        return current_user

    return checker


def require_capability(capability_code: str):
    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        authorization = AuthorizationService(db)

        if not authorization.has_capability(current_user, capability_code):
            raise HTTPException(
                status_code=403,
                detail=f"No tiene capacidad requerida: {capability_code}",
            )

        return current_user

    return checker
