from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=True)

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)

    recipient_user = Column(String(150), nullable=True)
    recipient_area = Column(String(150), nullable=True)

    priority = Column(String(50), default="medium")
    status = Column(String(50), default="unread")

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
