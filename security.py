from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), default="analyst")
    area = Column(String(150), nullable=True)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(150), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    category = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)


class Capability(Base):
    __tablename__ = "capabilities"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(150), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(Integer, index=True, nullable=False)
    permission_id = Column(Integer, index=True, nullable=False)

    granted_at = Column(DateTime, default=datetime.utcnow)


class RoleCapability(Base):
    __tablename__ = "role_capabilities"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(Integer, index=True, nullable=False)
    capability_id = Column(Integer, index=True, nullable=False)

    granted_at = Column(DateTime, default=datetime.utcnow)


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    role_id = Column(Integer, index=True, nullable=False)

    assigned_at = Column(DateTime, default=datetime.utcnow)


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    area_id = Column(Integer, index=True, nullable=True)

    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)


class UserTeam(Base):
    __tablename__ = "user_teams"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    team_id = Column(Integer, index=True, nullable=False)

    assigned_at = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)

    session_token = Column(String(500), nullable=True)

    ip_address = Column(String(100), nullable=True)
    user_agent = Column(Text, nullable=True)

    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)
