from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, index=True, nullable=False)

    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    direction = Column(String(50), default="input")
    allowed_extensions = Column(Text, nullable=True)

    is_required = Column(Boolean, default=False)
    is_ai_enabled = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class DocumentExtractionField(Base):
    __tablename__ = "document_extraction_fields"

    id = Column(Integer, primary_key=True, index=True)
    document_type_id = Column(Integer, index=True, nullable=False)

    source_name = Column(String(255), nullable=False)
    target_entity = Column(String(100), nullable=False)
    target_field = Column(String(150), nullable=False)

    extraction_type = Column(String(100), default="ai")
    is_required = Column(Boolean, default=False)

    instructions = Column(Text, nullable=True)


class ExcelColumnMapping(Base):
    __tablename__ = "excel_column_mappings"

    id = Column(Integer, primary_key=True, index=True)
    document_type_id = Column(Integer, index=True, nullable=False)

    sheet_name = Column(String(255), nullable=True)
    header_row = Column(Integer, default=1)

    column_name = Column(String(255), nullable=False)
    target_entity = Column(String(100), nullable=False)
    target_field = Column(String(150), nullable=False)

    is_required = Column(Boolean, default=False)
