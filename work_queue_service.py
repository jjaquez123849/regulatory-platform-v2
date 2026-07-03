from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.record import Record
from app.models.task import Task
from app.models.quality import QualityIssue
from app.models.document import Document


def get_work_queues(db: Session, current_user) -> dict:
    username = current_user.username
    user_area = current_user.area

    my_tasks_query = db.query(Task).filter(
        Task.is_deleted == False,
        Task.status != "completed",
    )

    if username:
        my_tasks_query = my_tasks_query.filter(Task.assigned_to == username)

    my_tasks = my_tasks_query.order_by(Task.due_date.asc()).all()

    area_tasks_query = db.query(Task).filter(
        Task.is_deleted == False,
        Task.status != "completed",
    )

    if user_area:
        area_tasks_query = area_tasks_query.filter(Task.assigned_area == user_area)

    area_tasks = area_tasks_query.order_by(Task.due_date.asc()).all()

    now = datetime.utcnow()
    soon = now + timedelta(days=3)

    due_soon = (
        db.query(Task)
        .filter(
            Task.is_deleted == False,
            Task.status != "completed",
            Task.due_date != None,
            Task.due_date >= now,
            Task.due_date <= soon,
        )
        .order_by(Task.due_date.asc())
        .all()
    )

    overdue = (
        db.query(Task)
        .filter(
            Task.is_deleted == False,
            Task.status != "completed",
            Task.due_date != None,
            Task.due_date < now,
        )
        .order_by(Task.due_date.asc())
        .all()
    )

    quality_issues = (
        db.query(QualityIssue)
        .filter(QualityIssue.is_resolved == False)
        .order_by(QualityIssue.created_at.desc())
        .all()
    )

    pending_documents = (
        db.query(Document)
        .filter(
            Document.is_deleted == False,
            Document.processing_status.in_([
                "uploaded",
                "classified",
                "pdf_extracted_with_errors",
                "text_extracted_with_errors",
                "unsupported_for_now",
            ]),
        )
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    open_records = (
        db.query(Record)
        .filter(
            Record.is_deleted == False,
            Record.is_complete == False,
        )
        .order_by(Record.updated_at.desc())
        .limit(100)
        .all()
    )

    return {
        "my_tasks": [_task_row(item) for item in my_tasks],
        "area_tasks": [_task_row(item) for item in area_tasks],
        "due_soon": [_task_row(item) for item in due_soon],
        "overdue": [_task_row(item) for item in overdue],
        "quality_issues": [_quality_issue_row(item) for item in quality_issues],
        "pending_documents": [_document_row(item) for item in pending_documents],
        "open_records": [_record_row(item) for item in open_records],
        "summary": {
            "my_tasks": len(my_tasks),
            "area_tasks": len(area_tasks),
            "due_soon": len(due_soon),
            "overdue": len(overdue),
            "quality_issues": len(quality_issues),
            "pending_documents": len(pending_documents),
            "open_records": len(open_records),
        },
    }


def _task_row(item: Task) -> dict:
    return {
        "id": item.id,
        "record_id": item.record_id,
        "title": item.title,
        "assigned_to": item.assigned_to,
        "assigned_area": item.assigned_area,
        "status": item.status,
        "priority": item.priority,
        "due_date": item.due_date,
        "created_at": item.created_at,
    }


def _quality_issue_row(item: QualityIssue) -> dict:
    return {
        "id": item.id,
        "record_id": item.record_id,
        "issue_type": item.issue_type,
        "severity": item.severity,
        "description": item.description,
        "created_at": item.created_at,
    }


def _document_row(item: Document) -> dict:
    return {
        "id": item.id,
        "record_id": item.record_id,
        "original_filename": item.original_filename,
        "file_extension": item.file_extension,
        "processing_status": item.processing_status,
        "uploaded_at": item.uploaded_at,
    }


def _record_row(item: Record) -> dict:
    return {
        "id": item.id,
        "process_id": item.process_id,
        "title": item.title,
        "summary": item.summary,
        "current_state_id": item.current_state_id,
        "is_complete": item.is_complete,
        "has_pending_items": item.has_pending_items,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }
