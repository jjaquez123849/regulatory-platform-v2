from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base


class DocumentUnderstandingResult(Base):
    __tablename__ = "document_understanding_results"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, index=True, nullable=False)
    record_id = Column(Integer, index=True, nullable=True)

    document_type = Column(String(150), nullable=True)
    issuer = Column(String(255), nullable=True)
    regulator = Column(String(255), nullable=True)
    subject = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)

    request_number = Column(String(150), nullable=True)
    request_date = Column(String(100), nullable=True)
    due_date = Column(String(100), nullable=True)

    entities_json = Column(Text, nullable=True)
    requests_json = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
