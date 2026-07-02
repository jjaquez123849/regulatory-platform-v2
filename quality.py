from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean

from app.core.database import Base


class QualityReview(Base):
    __tablename__ = "quality_reviews"

    id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, index=True, nullable=False)
    document_id = Column(Integer, index=True, nullable=True)

    status = Column(String(100), default="pending")
    score = Column(String(50), nullable=True)

    summary = Column(Text, nullable=True)

    has_missing_items = Column(Boolean, default=False)
    missing_items = Column(Text, nullable=True)

    reviewed_by = Column(String(150), nullable=True)
    reviewed_at = Column(DateTime, default=datetime.utcnow)


class QualityIssue(Base):
    __tablename__ = "quality_issues"

    id = Column(Integer, primary_key=True, index=True)

    review_id = Column(Integer, index=True, nullable=False)
    record_id = Column(Integer, index=True, nullable=False)

    issue_type = Column(String(150), nullable=False)
    severity = Column(String(100), default="medium")

    description = Column(Text, nullable=False)
    related_person_id = Column(Integer, nullable=True)
    related_request_item_id = Column(Integer, nullable=True)

    is_resolved = Column(Boolean, default=False)
    resolved_by = Column(String(150), nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
