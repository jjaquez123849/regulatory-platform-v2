from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ProcessField(Base):
    __tablename__ = "process_fields"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, index=True, nullable=False)

    name = Column(String(150), nullable=False)
    label = Column(String(255), nullable=False)
    field_type = Column(String(100), nullable=False)

    is_required = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    is_editable = Column(Boolean, default=True)
    is_exportable = Column(Boolean, default=True)

    display_order = Column(Integer, default=0)
    help_text = Column(Text, nullable=True)
    default_value = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class FieldOption(Base):
    __tablename__ = "field_options"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, index=True, nullable=False)

    value = Column(String(255), nullable=False)
    label = Column(String(255), nullable=False)

    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
