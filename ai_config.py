from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class AIConfiguration(Base):
    __tablename__ = "ai_configurations"

    id = Column(Integer, primary_key=True, index=True)

    process_id = Column(Integer, index=True, nullable=False)
    document_type_id = Column(Integer, index=True, nullable=True)

    name = Column(String(255), nullable=False)
    purpose = Column(String(150), nullable=False)

    instructions = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
