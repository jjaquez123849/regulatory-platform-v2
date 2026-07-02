from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=True)

    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)

    action = Column(String(150), nullable=False)
    details = Column(Text, nullable=True)

    performed_by = Column(String(150), nullable=True)
    performed_at = Column(DateTime, default=datetime.utcnow)
