from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class LocalAIModelConfig(Base):
    __tablename__ = "local_ai_model_configs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    engine_type = Column(String(100), default="rule_based")

    model_path = Column(Text, nullable=True)
    model_name = Column(String(255), nullable=True)

    context_size = Column(Integer, default=4096)
    temperature = Column(String(20), default="0.2")

    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
