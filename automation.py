from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)

    process_id = Column(Integer, index=True, nullable=False)

    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    trigger_event = Column(String(150), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class AutomationCondition(Base):
    __tablename__ = "automation_conditions"

    id = Column(Integer, primary_key=True, index=True)

    rule_id = Column(Integer, index=True, nullable=False)

    left_value = Column(String(255), nullable=False)
    operator = Column(String(50), nullable=False)
    right_value = Column(String(255), nullable=True)

    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class AutomationAction(Base):
    __tablename__ = "automation_actions"

    id = Column(Integer, primary_key=True, index=True)

    rule_id = Column(Integer, index=True, nullable=False)

    action_type = Column(String(150), nullable=False)
    action_payload = Column(Text, nullable=True)

    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
