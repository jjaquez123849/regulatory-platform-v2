from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base


class ExtractionLearningExample(Base):
    __tablename__ = "extraction_learning_examples"

    id = Column(Integer, primary_key=True, index=True)

    process_id = Column(Integer, index=True, nullable=True)
    document_type_id = Column(Integer, index=True, nullable=True)

    target_entity = Column(String(100), nullable=False)
    target_field = Column(String(150), nullable=False)

    original_value = Column(Text, nullable=True)
    corrected_value = Column(Text, nullable=True)

    source_context = Column(Text, nullable=True)
    source_file_extension = Column(String(50), nullable=True)

    created_by = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
