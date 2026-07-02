from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class WorkflowState(Base):
    __tablename__ = "workflow_states"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, index=True, nullable=False)

    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

    display_order = Column(Integer, default=0)
    color = Column(String(50), nullable=True)

    is_initial = Column(Boolean, default=False)
    is_final = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class WorkflowTransition(Base):
    __tablename__ = "workflow_transitions"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, index=True, nullable=False)

    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

    from_state_id = Column(Integer, index=True, nullable=False)
    to_state_id = Column(Integer, index=True, nullable=False)

    requires_comment = Column(Boolean, default=False)
    requires_checklist_completed = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorkflowHistory(Base):
    __tablename__ = "workflow_history"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, index=True, nullable=False)

    transition_id = Column(Integer, nullable=True)
    from_state_id = Column(Integer, nullable=True)
    to_state_id = Column(Integer, nullable=False)

    comment = Column(Text, nullable=True)
    performed_by = Column(String(150), nullable=True)
    performed_at = Column(DateTime, default=datetime.utcnow)
