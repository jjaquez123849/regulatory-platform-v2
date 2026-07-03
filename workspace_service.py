import json

from sqlalchemy.orm import Session

from app.domains.iam.services.authorization_service import AuthorizationService
from app.models.audit import AuditLog
from app.models.comment import Comment
from app.models.document import Document
from app.models.document_understanding import DocumentUnderstandingResult
from app.models.notification import Notification
from app.models.quality import QualityIssue, QualityReview
from app.models.record import Record, RecordPerson, RecordRequestItem, RecordValue
from app.models.task import Task
from app.models.workflow import WorkflowHistory, WorkflowState


def get_record_workspace(db: Session, record_id: int, current_user) -> dict:
    record = (
        db.query(Record)
        .filter(Record.id == record_id, Record.is_deleted == False)
        .first()
    )

    if not record:
        raise ValueError("Registro no encontrado.")

    authorization = AuthorizationService(db)

    current_state = None
    if record.current_state_id:
        current_state = (
            db.query(WorkflowState)
            .filter(WorkflowState.id == record.current_state_id)
            .first()
        )

    values = db.query(RecordValue).filter(RecordValue.record_id == record.id).all()
    people = db.query(RecordPerson).filter(RecordPerson.record_id == record.id).all()
    request_items = (
        db.query(RecordRequestItem)
        .filter(RecordRequestItem.record_id == record.id)
        .all()
    )

    documents = (
        db.query(Document)
        .filter(Document.record_id == record.id, Document.is_deleted == False)
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(Task.record_id == record.id, Task.is_deleted == False)
        .order_by(Task.created_at.desc())
        .all()
    )

    quality_reviews = (
        db.query(QualityReview)
        .filter(QualityReview.record_id == record.id)
        .order_by(QualityReview.reviewed_at.desc())
        .all()
    )

    quality_issues = (
        db.query(QualityIssue)
        .filter(QualityIssue.record_id == record.id)
        .order_by(QualityIssue.created_at.desc())
        .all()
    )

    workflow_history = (
        db.query(WorkflowHistory)
        .filter(WorkflowHistory.record_id == record.id)
        .order_by(WorkflowHistory.performed_at.desc())
        .all()
    )

    audit_items = (
        db.query(AuditLog)
        .filter(AuditLog.record_id == record.id)
        .order_by(AuditLog.created_at.desc())
        .limit(100)
        .all()
    )

    notifications = (
        db.query(Notification)
        .filter(Notification.record_id == record.id, Notification.is_deleted == False)
        .order_by(Notification.created_at.desc())
        .all()
    )

    understandings = (
        db.query(DocumentUnderstandingResult)
        .filter(DocumentUnderstandingResult.record_id == record.id)
        .order_by(DocumentUnderstandingResult.created_at.desc())
        .all()
    )

    comments = (
        db.query(Comment)
        .filter(Comment.record_id == record.id, Comment.is_deleted == False)
        .order_by(Comment.created_at.desc())
        .all()
    )

    timeline = []

    for item in workflow_history:
        timeline.append({
            "id": f"workflow-{item.id}",
            "title": "Cambio de estado",
            "description": item.comment,
            "date": item.performed_at,
            "type": "workflow",
        })

    for item in documents:
        timeline.append({
            "id": f"document-{item.id}",
            "title": "Documento cargado",
            "description": item.original_filename,
            "date": item.uploaded_at,
            "type": "document",
        })

    for item in quality_reviews:
        timeline.append({
            "id": f"quality-{item.id}",
            "title": "Revisión de calidad",
            "description": item.summary,
            "date": item.reviewed_at,
            "type": "quality",
        })

    for item in comments:
        timeline.append({
            "id": f"comment-{item.id}",
            "title": "Comentario",
            "description": item.comment_text,
            "date": item.created_at,
            "type": "comment",
        })

    timeline = sorted(timeline, key=lambda item: item["date"] or "", reverse=True)

    layout = [
        {
            "id": "ai",
            "code": "ai",
            "title": "Resumen IA",
            "description": "Hallazgos y resumen inteligente del expediente.",
            "order": 1,
            "visible": True,
            "widgets": [{"id": "ai_summary", "widget": "AI_SUMMARY"}],
        },
        {
            "id": "timeline",
            "code": "timeline",
            "title": "Timeline",
            "description": "Eventos principales del expediente.",
            "order": 2,
            "visible": True,
            "widgets": [{"id": "timeline", "widget": "TIMELINE"}],
        },
        {
            "id": "log",
            "code": "log",
            "title": "Log",
            "description": "Información oficial del expediente.",
            "order": 3,
            "visible": True,
            "widgets": [{"id": "log", "widget": "LOG"}],
        },
        {
            "id": "people_requests",
            "code": "people_requests",
            "title": "Personas y solicitudes",
            "description": "Personas detectadas y requerimientos asociados.",
            "order": 4,
            "visible": True,
            "widgets": [
                {"id": "people", "widget": "PEOPLE"},
                {"id": "requests", "widget": "REQUESTS"},
            ],
        },
        {
            "id": "documents",
            "code": "documents",
            "title": "Documentos",
            "description": "Documentos cargados, procesados y comprendidos.",
            "order": 5,
            "visible": True,
            "widgets": [{"id": "documents", "widget": "DOCUMENTS"}],
        },
        {
            "id": "tasks",
            "code": "tasks",
            "title": "Tareas",
            "description": "Tareas operativas del expediente.",
            "order": 6,
            "visible": True,
            "widgets": [{"id": "tasks", "widget": "TASKS"}],
        },
        {
            "id": "quality",
            "code": "quality",
            "title": "Calidad",
            "description": "Revisiones y observaciones de calidad.",
            "order": 7,
            "visible": True,
            "widgets": [{"id": "quality", "widget": "QUALITY"}],
        },
        {
            "id": "comments",
            "code": "comments",
            "title": "Comentarios",
            "description": "Notas internas del expediente.",
            "order": 8,
            "visible": True,
            "widgets": [{"id": "comments", "widget": "COMMENTS"}],
        },
        {
            "id": "audit",
            "code": "audit",
            "title": "Auditoría",
            "description": "Historial técnico de acciones.",
            "order": 9,
            "visible": True,
            "widgets": [{"id": "audit", "widget": "AUDIT"}],
        },
    ]

    return {
        "record": {
            "id": record.id,
            "process_id": record.process_id,
            "title": record.title,
            "summary": record.summary,
            "state": current_state.name if current_state else None,
            "state_id": record.current_state_id,
            "is_complete": record.is_complete,
            "has_pending_items": record.has_pending_items,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
            "closed_at": record.closed_at,
        },
        "values": [
            {
                "id": item.id,
                "field_id": item.field_id,
                "value_text": item.value_text,
                "value_number": item.value_number,
                "value_date": item.value_date,
                "value_boolean": item.value_boolean,
            }
            for item in values
        ],
        "people": [
            {
                "id": item.id,
                "full_name": item.full_name,
                "identification": item.identification,
                "identification_type": item.identification_type,
                "role": item.role,
                "notes": item.notes,
            }
            for item in people
        ],
        "request_items": [
            {
                "id": item.id,
                "person_id": item.person_id,
                "request_type": item.request_type,
                "description": item.description,
                "status": item.status,
                "pending_reason": item.pending_reason,
                "response_summary": item.response_summary,
                "is_answered": item.is_answered,
            }
            for item in request_items
        ],
        "documents": [
            {
                "id": item.id,
                "document_type_id": item.document_type_id,
                "original_filename": item.original_filename,
                "file_extension": item.file_extension,
                "direction": item.direction,
                "processing_status": item.processing_status,
                "ai_summary": item.ai_summary,
                "ai_confidence": item.ai_confidence,
                "uploaded_at": item.uploaded_at,
            }
            for item in documents
        ],
        "tasks": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "assigned_to": item.assigned_to,
                "assigned_area": item.assigned_area,
                "status": item.status,
                "priority": item.priority,
                "due_date": item.due_date,
                "created_at": item.created_at,
            }
            for item in tasks
        ],
        "quality": {
            "reviews": [
                {
                    "id": item.id,
                    "status": item.status,
                    "score": item.score,
                    "summary": item.summary,
                    "has_missing_items": item.has_missing_items,
                    "reviewed_at": item.reviewed_at,
                }
                for item in quality_reviews
            ],
            "issues": [
                {
                    "id": item.id,
                    "issue_type": item.issue_type,
                    "severity": item.severity,
                    "description": item.description,
                    "is_resolved": item.is_resolved,
                    "created_at": item.created_at,
                }
                for item in quality_issues
            ],
        },
        "timeline": timeline,
        "audit": [
            {
                "id": item.id,
                "entity_type": item.entity_type,
                "entity_id": item.entity_id,
                "action": item.action,
                "details": item.details,
                "performed_by": item.performed_by,
                "created_at": item.created_at,
            }
            for item in audit_items
        ],
        "notifications": [
            {
                "id": item.id,
                "title": item.title,
                "message": item.message,
                "priority": item.priority,
                "status": item.status,
                "created_at": item.created_at,
            }
            for item in notifications
        ],
        "understandings": [
            {
                "id": item.id,
                "issuer": item.issuer,
                "regulator": item.regulator,
                "summary": item.summary,
                "request_number": item.request_number,
                "due_date": item.due_date,
                "entities": json.loads(item.entities_json or "[]"),
                "requests": json.loads(item.requests_json or "[]"),
                "created_at": item.created_at,
            }
            for item in understandings
        ],
        "comments": [
            {
                "id": item.id,
                "comment_text": item.comment_text,
                "comment_type": item.comment_type,
                "created_by": item.created_by,
                "created_at": item.created_at,
            }
            for item in comments
        ],
        "permissions": authorization.get_user_permissions(current_user),
        "capabilities": authorization.get_user_capabilities(current_user),
        "allowed_actions": authorization.get_record_allowed_actions(current_user, record),
        "layout": layout,
    }
