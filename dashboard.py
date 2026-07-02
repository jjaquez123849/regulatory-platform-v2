from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.record import Record
from app.models.task import Task
from app.models.quality import QualityIssue
from app.models.document import Document


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    records = (
        db.query(Record)
        .filter(Record.is_deleted == False)
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(Task.is_deleted == False)
        .all()
    )

    open_quality_issues = (
        db.query(QualityIssue)
        .filter(QualityIssue.is_resolved == False)
        .count()
    )

    documents_pending = (
        db.query(Document)
        .filter(
            Document.is_deleted == False,
            Document.processing_status.in_(["pending", "uploaded"])
        )
        .count()
    )

    now = datetime.utcnow()

    overdue_tasks = [
        task for task in tasks
        if task.due_date
        and task.due_date < now
        and task.status not in ["completed", "cancelled"]
    ]

    return {
        "records_total": len(records),
        "records_open": sum(1 for item in records if not item.closed_at),
        "records_closed": sum(1 for item in records if item.closed_at),
        "records_complete": sum(1 for item in records if item.is_complete),
        "records_with_pending_items": sum(1 for item in records if item.has_pending_items),
        "tasks_total": len(tasks),
        "tasks_pending": sum(1 for item in tasks if item.status == "pending"),
        "tasks_in_progress": sum(1 for item in tasks if item.status == "in_progress"),
        "tasks_completed": sum(1 for item in tasks if item.status == "completed"),
        "tasks_overdue": len(overdue_tasks),
        "quality_open_issues": open_quality_issues,
        "documents_pending_processing": documents_pending
    }


@router.get("/records-by-state")
def records_by_state(db: Session = Depends(get_db)):
    records = (
        db.query(Record)
        .filter(Record.is_deleted == False)
        .all()
    )

    result = {}

    for record in records:
        state_id = record.current_state_id or "sin_estado"
        result[str(state_id)] = result.get(str(state_id), 0) + 1

    return result


@router.get("/critical")
def critical_items(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    overdue_tasks = (
        db.query(Task)
        .filter(
            Task.is_deleted == False,
            Task.due_date < now,
            Task.status.notin_(["completed", "cancelled"])
        )
        .order_by(Task.due_date.asc())
        .limit(50)
        .all()
    )

    quality_issues = (
        db.query(QualityIssue)
        .filter(QualityIssue.is_resolved == False)
        .order_by(QualityIssue.created_at.desc())
        .limit(50)
        .all()
    )

    return {
        "overdue_tasks": [
            {
                "id": task.id,
                "record_id": task.record_id,
                "title": task.title,
                "assigned_to": task.assigned_to,
                "assigned_area": task.assigned_area,
                "priority": task.priority,
                "due_date": task.due_date
            }
            for task in overdue_tasks
        ],
        "quality_issues": [
            {
                "id": issue.id,
                "record_id": issue.record_id,
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.description,
                "created_at": issue.created_at
            }
            for issue in quality_issues
        ]
    }
