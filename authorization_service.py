from sqlalchemy.orm import Session

from app.models.security import (
    User,
    UserRole,
    Role,
    RolePermission,
    Permission,
    RoleCapability,
    Capability,
    UserTeam,
    Team,
)


class AuthorizationService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_roles(self, user: User) -> list[str]:
        if user.is_superuser:
            return ["superuser"]

        rows = (
            self.db.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(
                UserRole.user_id == user.id,
                Role.is_active == True,
            )
            .all()
        )

        roles = [item.code for item in rows]

        if user.role and user.role not in roles:
            roles.append(user.role)

        return roles

    def get_user_permissions(self, user: User) -> list[str]:
        if user.is_superuser:
            return ["*"]

        permissions = (
            self.db.query(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(
                UserRole.user_id == user.id,
                Role.is_active == True,
                Permission.is_active == True,
            )
            .all()
        )

        result = sorted(set(item.code for item in permissions))
        legacy_role_permissions = self._legacy_role_permissions(user.role)

        return sorted(set(result + legacy_role_permissions))

    def get_user_capabilities(self, user: User) -> list[str]:
        if user.is_superuser:
            return ["*"]

        capabilities = (
            self.db.query(Capability)
            .join(RoleCapability, RoleCapability.capability_id == Capability.id)
            .join(Role, Role.id == RoleCapability.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(
                UserRole.user_id == user.id,
                Role.is_active == True,
                Capability.is_active == True,
            )
            .all()
        )

        return sorted(set(item.code for item in capabilities))

    def get_user_teams(self, user: User) -> list[str]:
        teams = (
            self.db.query(Team)
            .join(UserTeam, UserTeam.team_id == Team.id)
            .filter(
                UserTeam.user_id == user.id,
                Team.is_active == True,
            )
            .all()
        )

        return sorted(set(item.code for item in teams))

    def can(self, user: User, permission_code: str) -> bool:
        permissions = self.get_user_permissions(user)
        return "*" in permissions or permission_code in permissions

    def has_capability(self, user: User, capability_code: str) -> bool:
        capabilities = self.get_user_capabilities(user)
        return "*" in capabilities or capability_code in capabilities

    def get_effective_access(self, user: User) -> dict:
        return {
            "user_id": user.id,
            "username": user.username,
            "roles": self.get_user_roles(user),
            "permissions": self.get_user_permissions(user),
            "capabilities": self.get_user_capabilities(user),
            "teams": self.get_user_teams(user),
        }

    def get_record_allowed_actions(self, user: User, record=None) -> list[str]:
        permissions = self.get_user_permissions(user)

        if "*" in permissions:
            return [
                "VIEW_RECORD",
                "EDIT_LOG",
                "UPLOAD_DOCUMENT",
                "CLASSIFY_DOCUMENT",
                "UNDERSTAND_DOCUMENT",
                "PROCESS_DOCUMENT",
                "APPLY_EXTRACTION",
                "RUN_QUALITY",
                "RESOLVE_QUALITY_ISSUE",
                "CREATE_TASK",
                "ASSIGN_TASK",
                "COMPLETE_TASK",
                "CHANGE_WORKFLOW",
                "CREATE_COMMENT",
                "VIEW_AUDIT",
            ]

        mapping = {
            "RECORD_VIEW": "VIEW_RECORD",
            "RECORD_EDIT": "EDIT_LOG",
            "DOCUMENT_UPLOAD": "UPLOAD_DOCUMENT",
            "DOCUMENT_CLASSIFY": "CLASSIFY_DOCUMENT",
            "DOCUMENT_UNDERSTAND": "UNDERSTAND_DOCUMENT",
            "DOCUMENT_PROCESS": "PROCESS_DOCUMENT",
            "EXTRACTION_APPLY": "APPLY_EXTRACTION",
            "QUALITY_RUN": "RUN_QUALITY",
            "QUALITY_RESOLVE": "RESOLVE_QUALITY_ISSUE",
            "TASK_CREATE": "CREATE_TASK",
            "TASK_ASSIGN": "ASSIGN_TASK",
            "TASK_COMPLETE": "COMPLETE_TASK",
            "WORKFLOW_CHANGE": "CHANGE_WORKFLOW",
            "COMMENT_CREATE": "CREATE_COMMENT",
            "AUDIT_VIEW": "VIEW_AUDIT",
        }

        return sorted(
            set(action for permission, action in mapping.items() if permission in permissions)
        )

    def _legacy_role_permissions(self, role: str | None) -> list[str]:
        if not role:
            return []

        role = role.lower()

        legacy = {
            "admin": ["*"],
            "supervisor": [
                "AI_VIEW",
                "RECORD_VIEW",
                "RECORD_EDIT",
                "DOCUMENT_VIEW",
                "DOCUMENT_UPLOAD",
                "DOCUMENT_CLASSIFY",
                "DOCUMENT_UNDERSTAND",
                "DOCUMENT_PROCESS",
                "EXTRACTION_APPLY",
                "TASK_VIEW",
                "TASK_CREATE",
                "TASK_ASSIGN",
                "TASK_COMPLETE",
                "QUALITY_VIEW",
                "QUALITY_RUN",
                "QUALITY_RESOLVE",
                "WORKFLOW_VIEW",
                "WORKFLOW_CHANGE",
                "COMMENT_CREATE",
                "AUDIT_VIEW",
                "DASHBOARD_VIEW",
            ],
            "analyst": [
                "AI_VIEW",
                "RECORD_VIEW",
                "RECORD_EDIT",
                "DOCUMENT_VIEW",
                "DOCUMENT_UPLOAD",
                "DOCUMENT_CLASSIFY",
                "DOCUMENT_UNDERSTAND",
                "DOCUMENT_PROCESS",
                "EXTRACTION_APPLY",
                "TASK_VIEW",
                "TASK_CREATE",
                "TASK_COMPLETE",
                "COMMENT_CREATE",
            ],
            "quality": [
                "AI_VIEW",
                "RECORD_VIEW",
                "DOCUMENT_VIEW",
                "TASK_VIEW",
                "QUALITY_VIEW",
                "QUALITY_RUN",
                "QUALITY_RESOLVE",
                "COMMENT_CREATE",
                "AUDIT_VIEW",
            ],
            "viewer": [
                "AI_VIEW",
                "RECORD_VIEW",
                "DOCUMENT_VIEW",
                "TASK_VIEW",
                "QUALITY_VIEW",
                "DASHBOARD_VIEW",
            ],
        }

        return legacy.get(role, [])
