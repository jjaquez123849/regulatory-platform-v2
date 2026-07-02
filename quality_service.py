from datetime import datetime

from sqlalchemy.orm import Session

from app.models.quality import QualityReview, QualityIssue
from app.models.record import RecordPerson, RecordRequestItem
from app.models.document import Document
from app.models.audit import AuditLog
from app.services.record_service import get_record


def run_quality_review(
    db: Session,
    record_id: int,
    document_id: int | None = None,
    reviewed_by: str | None = None
) -> QualityReview:
    record = get_record(db, record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    if document_id is not None:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError("Documento no encontrado.")

    people = db.query(RecordPerson).filter(RecordPerson.record_id == record.id).all()
    request_items = db.query(RecordRequestItem).filter(RecordRequestItem.record_id == record.id).all()

    issues = []

    if not people:
        issues.append({
            "issue_type": "missing_person",
            "severity": "high",
            "description": "No se identificaron personas asociadas al requerimiento.",
            "person_id": None,
            "request_item_id": None
        })

    if not request_items:
        issues.append({
            "issue_type": "missing_request_items",
            "severity": "high",
            "description": "No se identificaron solicitudes específicas dentro del requerimiento.",
            "person_id": None,
            "request_item_id": None
        })

    for person in people:
        if not person.identification:
            issues.append({
                "issue_type": "missing_identification",
                "severity": "medium",
                "description": f"La persona '{person.full_name}' no tiene identificación registrada.",
                "person_id": person.id,
                "request_item_id": None
            })

    for item in request_items:
        if not item.is_answered:
            issues.append({
                "issue_type": "unanswered_request_item",
                "severity": "high",
                "description": f"La solicitud '{item.request_type}' no está marcada como respondida.",
                "person_id": item.person_id,
                "request_item_id": item.id
            })

        if item.pending_reason:
            issues.append({
                "issue_type": "pending_reason",
                "severity": "medium",
                "description": f"La solicitud '{item.request_type}' tiene pendiente: {item.pending_reason}",
                "person_id": item.person_id,
                "request_item_id": item.id
            })

    if issues:
        status = "observed"
        score = "incomplete"
        summary = f"Se detectaron {len(issues)} observaciones o faltantes."
        has_missing_items = True
        missing_items = "\n".join([issue["description"] for issue in issues])
    else:
        status = "approved"
        score = "complete"
        summary = "La revisión no detectó faltantes."
        has_missing_items = False
        missing_items = None

    review = QualityReview(
        record_id=record.id,
        document_id=document_id,
        status=status,
        score=score,
        summary=summary,
        has_missing_items=has_missing_items,
        missing_items=missing_items,
        reviewed_by=reviewed_by,
        reviewed_at=datetime.utcnow()
    )

    db.add(review)
    db.flush()

    for issue in issues:
        db.add(
            QualityIssue(
                review_id=review.id,
                record_id=record.id,
                issue_type=issue["issue_type"],
                severity=issue["severity"],
                description=issue["description"],
                related_person_id=issue["person_id"],
                related_request_item_id=issue["request_item_id"],
                created_at=datetime.utcnow()
            )
        )

    record.has_pending_items = has_missing_items
    record.is_complete = not has_missing_items
    record.updated_at = datetime.utcnow()

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="quality_review",
            entity_id=review.id,
            action="RUN_QUALITY_REVIEW",
            details=summary,
            performed_by=reviewed_by
        )
    )

    db.commit()
    db.refresh(review)

    return review


def list_quality_reviews(db: Session, record_id: int) -> list[QualityReview]:
    return (
        db.query(QualityReview)
        .filter(QualityReview.record_id == record_id)
        .order_by(QualityReview.reviewed_at.desc())
        .all()
    )


def list_quality_issues(
    db: Session,
    record_id: int,
    only_open: bool = True
) -> list[QualityIssue]:
    query = db.query(QualityIssue).filter(QualityIssue.record_id == record_id)

    if only_open:
        query = query.filter(QualityIssue.is_resolved == False)

    return query.order_by(QualityIssue.created_at.desc()).all()


def resolve_quality_issue(
    db: Session,
    issue_id: int,
    resolved_by: str | None = None,
    resolution_comment: str | None = None
) -> QualityIssue | None:
    issue = db.query(QualityIssue).filter(QualityIssue.id == issue_id).first()

    if not issue:
        return None

    issue.is_resolved = True
    issue.resolved_by = resolved_by
    issue.resolved_at = datetime.utcnow()

    db.add(
        AuditLog(
            record_id=issue.record_id,
            entity_type="quality_issue",
            entity_id=issue.id,
            action="RESOLVE_QUALITY_ISSUE",
            details=resolution_comment or f"Observación resuelta: {issue.description}",
            performed_by=resolved_by
        )
    )

    open_issues = (
        db.query(QualityIssue)
        .filter(
            QualityIssue.record_id == issue.record_id,
            QualityIssue.is_resolved == False,
            QualityIssue.id != issue.id
        )
        .count()
    )

    record = get_record(db, issue.record_id)

    if record and open_issues == 0:
        record.has_pending_items = False
        record.is_complete = True
        record.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(issue)

    return issue
