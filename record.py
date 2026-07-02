from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)

    process_id = Column(Integer, index=True, nullable=False)
    current_state_id = Column(Integer, index=True, nullable=True)

    title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)

    source_channel = Column(String(100), nullable=True)

    is_complete = Column(Boolean, default=False)
    has_pending_items = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    created_by = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)


class RecordValue(Base):
    __tablename__ = "record_values"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)
    field_id = Column(Integer, index=True, nullable=False)

    value_text = Column(Text, nullable=True)
    value_number = Column(String(100), nullable=True)
    value_date = Column(String(50), nullable=True)
    value_boolean = Column(Boolean, nullable=True)

    updated_at = Column(DateTime, default=datetime.utcnow)


class RecordPerson(Base):
    __tablename__ = "record_persons"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)

    full_name = Column(String(255), nullable=False)
    identification = Column(String(100), nullable=True)
    identification_type = Column(String(100), nullable=True)

    role = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    confidence_score = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class RecordRequestItem(Base):
    __tablename__ = "record_request_items"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)
    person_id = Column(Integer, index=True, nullable=True)

    request_type = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String(100), default="pending")
    pending_reason = Column(Text, nullable=True)

    response_summary = Column(Text, nullable=True)
    is_answered = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
