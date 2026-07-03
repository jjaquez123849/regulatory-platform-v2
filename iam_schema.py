from typing import Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class RoleResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class PermissionCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True


class PermissionResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class CapabilityCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class CapabilityResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class AreaCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class AreaResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    code: str
    name: str
    area_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True


class TeamResponse(BaseModel):
    id: int
    code: str
    name: str
    area_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class AssignRolePermissionRequest(BaseModel):
    role_id: int
    permission_id: int


class AssignRoleCapabilityRequest(BaseModel):
    role_id: int
    capability_id: int


class AssignUserRoleRequest(BaseModel):
    user_id: int
    role_id: int


class AssignUserTeamRequest(BaseModel):
    user_id: int
    team_id: int


class EffectiveAccessResponse(BaseModel):
    user_id: int
    username: str
    roles: list[str]
    permissions: list[str]
    capabilities: list[str]
    teams: list[str]
