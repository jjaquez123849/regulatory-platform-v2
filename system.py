from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.configuration import Process
from app.models.document import Document
from app.models.record import Record
from app.models.task import Task
from app.models.quality import QualityIssue
from app.models.notification import Notification


router = APIRouter(
    prefix="/system",
    tags=["System"]
)


@router.get("/diagnostics")
def system_diagnostics(db: Session = Depends(get_db)):
    database_status = "ok"

    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    base_dir = Path(__file__).resolve().parents[2]
    uploads_dir = base_dir / "data" / "uploads"

    uploads_dir.mkdir(parents=True, exist_ok=True)

    return {
        "status": "ok" if database_status == "ok" else "warning",
        "database": {
            "engine": "sqlite",
            "status": database_status
        },
        "storage": {
            "uploads_dir": str(uploads_dir),
            "uploads_dir_exists": uploads_dir.exists()
        },
        "counts": {
            "processes": db.query(Process).count(),
            "records": db.query(Record).filter(Record.is_deleted == False).count(),
            "documents": db.query(Document).filter(Document.is_deleted == False).count(),
            "tasks": db.query(Task).filter(Task.is_deleted == False).count(),
            "open_quality_issues": db.query(QualityIssue).filter(QualityIssue.is_resolved == False).count(),
            "unread_notifications": db.query(Notification).filter(Notification.status == "unread").count()
        },
        "modules": {
            "admin": True,
            "records": True,
            "documents": True,
            "document_classification": True,
            "document_understanding": True,
            "extraction": True,
            "quality": True,
            "workflow": True,
            "automation": True,
            "notifications": True
        }
    }
