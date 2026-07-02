from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    assigned_to = Column(String(150), nullable=True)
    assigned_area = Column(String(150), nullable=True)

    status = Column(String(100), default="pending", index=True)
    priority = Column(String(100), default="medium")

    due_date = Column(DateTime, nullable=True)

    is_deleted = Column(Boolean, default=False)

    created_by = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    completed_by = Column(String(150), nullable=True)
    completed_at = Column(DateTime, nullable=True)
