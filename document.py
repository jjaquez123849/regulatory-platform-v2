from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=True)
    document_type_id = Column(Integer, index=True, nullable=True)

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)

    file_extension = Column(String(50), nullable=True)
    mime_type = Column(String(150), nullable=True)

    direction = Column(String(50), default="input")
    processing_status = Column(String(100), default="pending")

    ai_summary = Column(Text, nullable=True)
    ai_confidence = Column(String(50), nullable=True)

    is_deleted = Column(Boolean, default=False)

    uploaded_by = Column(String(150), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class DocumentExtractionResult(Base):
    __tablename__ = "document_extraction_results"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, index=True, nullable=False)
    record_id = Column(Integer, index=True, nullable=True)

    target_entity = Column(String(100), nullable=False)
    target_field = Column(String(150), nullable=False)

    extracted_value = Column(Text, nullable=True)
    normalized_value = Column(Text, nullable=True)

    confidence_score = Column(String(50), nullable=True)
    status = Column(String(100), default="proposed")

    reviewed_by = Column(String(150), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
