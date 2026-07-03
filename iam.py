from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user, require_admin
from app.core.database import get_db
from app.domains.iam.services.authorization_service import AuthorizationService
from app.models.security import (
    User,
    Role,
    Permission,
    Capability,
    Area,
    Team,
    RolePermission,
    RoleCapability,
    UserRole,
    UserTeam,
)
from app.schemas.iam_schema import (
    RoleCreate,
    RoleResponse,
    PermissionCreate,
    PermissionResponse,
    CapabilityCreate,
    CapabilityResponse,
    AreaCreate,
    AreaResponse,
    TeamCreate,
    TeamResponse,
    AssignRolePermissionRequest,
    AssignRoleCapabilityRequest,
    AssignUserRoleRequest,
    AssignUserTeamRequest,
    EffectiveAccessResponse,
)


router = APIRouter(
    prefix="/iam",
    tags=["IAM"]
)


@router.get("/me/effective-access", response_model=EffectiveAccessResponse)
def read_my_effective_access(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AuthorizationService(db)
    return service.get_effective_access(current_user)


@router.get("/records/{record_id}/allowed-actions")
def read_record_allowed_actions(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.record import Record

    record = (
        db.query(Record)
        .filter(
            Record.id == record_id,
            Record.is_deleted == False,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")

    service = AuthorizationService(db)

    return {
        "record_id": record.id,
        "allowed_actions": service.get_record_allowed_actions(
            user=current_user,
            record=record,
        ),
    }


@router.post("/roles", response_model=RoleResponse)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Role).filter(Role.code == payload.code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese código.")

    role = Role(**payload.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)

    return role


@router.get("/roles", response_model=list[RoleResponse])
def read_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Role).order_by(Role.code.asc()).all()


@router.post("/permissions", response_model=PermissionResponse)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Permission).filter(Permission.code == payload.code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un permiso con ese código.")

    permission = Permission(**payload.model_dump())
    db.add(permission)
    db.commit()
    db.refresh(permission)

    return permission


@router.get("/permissions", response_model=list[PermissionResponse])
def read_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Permission).order_by(Permission.category.asc(), Permission.code.asc()).all()


@router.post("/capabilities", response_model=CapabilityResponse)
def create_capability(
    payload: CapabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Capability).filter(Capability.code == payload.code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una capacidad con ese código.")

    capability = Capability(**payload.model_dump())
    db.add(capability)
    db.commit()
    db.refresh(capability)

    return capability


@router.get("/capabilities", response_model=list[CapabilityResponse])
def read_capabilities(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Capability).order_by(Capability.code.asc()).all()


@router.post("/areas", response_model=AreaResponse)
def create_area(
    payload: AreaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Area).filter(Area.code == payload.code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un área con ese código.")

    area = Area(**payload.model_dump())
    db.add(area)
    db.commit()
    db.refresh(area)

    return area


@router.get("/areas", response_model=list[AreaResponse])
def read_areas(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Area).order_by(Area.code.asc()).all()


@router.post("/teams", response_model=TeamResponse)
def create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = db.query(Team).filter(Team.code == payload.code).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un equipo con ese código.")

    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get("/teams", response_model=list[TeamResponse])
def read_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return db.query(Team).order_by(Team.code.asc()).all()


@router.post("/roles/permissions")
def assign_permission_to_role(
    payload: AssignRolePermissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == payload.role_id,
            RolePermission.permission_id == payload.permission_id,
        )
        .first()
    )

    if existing:
        return {"status": "exists"}

    item = RolePermission(
        role_id=payload.role_id,
        permission_id=payload.permission_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"status": "assigned", "id": item.id}


@router.post("/roles/capabilities")
def assign_capability_to_role(
    payload: AssignRoleCapabilityRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = (
        db.query(RoleCapability)
        .filter(
            RoleCapability.role_id == payload.role_id,
            RoleCapability.capability_id == payload.capability_id,
        )
        .first()
    )

    if existing:
        return {"status": "exists"}

    item = RoleCapability(
        role_id=payload.role_id,
        capability_id=payload.capability_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"status": "assigned", "id": item.id}


@router.post("/users/roles")
def assign_role_to_user(
    payload: AssignUserRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == payload.user_id,
            UserRole.role_id == payload.role_id,
        )
        .first()
    )

    if existing:
        return {"status": "exists"}

    item = UserRole(
        user_id=payload.user_id,
        role_id=payload.role_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"status": "assigned", "id": item.id}


@router.post("/users/teams")
def assign_team_to_user(
    payload: AssignUserTeamRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing = (
        db.query(UserTeam)
        .filter(
            UserTeam.user_id == payload.user_id,
            UserTeam.team_id == payload.team_id,
        )
        .first()
    )

    if existing:
        return {"status": "exists"}

    item = UserTeam(
        user_id=payload.user_id,
        team_id=payload.team_id,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"status": "assigned", "id": item.id}
