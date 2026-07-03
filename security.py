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


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    role = Column(String(50), index=True, nullable=False)
    permission_code = Column(String(150), nullable=False)

    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
