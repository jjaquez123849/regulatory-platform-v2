from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)

    comment_text = Column(Text, nullable=False)
    comment_type = Column(String(50), default="general")

    created_by = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)
