from datetime import datetime

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.audit import AuditLog
from app.services.record_service import get_record


VALID_TASK_STATUSES = ["pending", "in_progress", "completed", "cancelled"]


def create_task(db: Session, data: dict) -> Task:
    record = get_record(db, data["record_id"])

    if not record:
        raise ValueError("Registro no encontrado.")

    task = Task(
        record_id=data["record_id"],
        title=data["title"],
        description=data.get("description"),
        assigned_to=data.get("assigned_to"),
        assigned_area=data.get("assigned_area"),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        due_date=data.get("due_date"),
        created_by=data.get("created_by"),
        created_at=datetime.utcnow()
    )

    db.add(task)
    db.flush()

    db.add(
        AuditLog(
            record_id=task.record_id,
            entity_type="task",
            entity_id=task.id,
            action="CREATE_TASK",
            details=f"Tarea creada: {task.title}",
            performed_by=task.created_by
        )
    )

    db.commit()
    db.refresh(task)

    return task


def list_tasks(
    db: Session,
    record_id: int | None = None,
    status: str | None = None,
    assigned_to: str | None = None,
    assigned_area: str | None = None
) -> list[Task]:
    query = db.query(Task).filter(Task.is_deleted == False)

    if record_id is not None:
        query = query.filter(Task.record_id == record_id)

    if status:
        query = query.filter(Task.status == status)

    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    if assigned_area:
        query = query.filter(Task.assigned_area == assigned_area)

    return query.order_by(Task.created_at.desc()).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.is_deleted == False
        )
        .first()
    )


def update_task(db: Session, task_id: int, data: dict) -> Task | None:
    task = get_task(db, task_id)

    if not task:
        return None

    if data.get("status") is not None:
        if data["status"] not in VALID_TASK_STATUSES:
            raise ValueError(f"Estado de tarea inválido: {data['status']}")

        task.status = data["status"]

        if data["status"] == "completed":
            task.completed_by = data.get("completed_by")
            task.completed_at = datetime.utcnow()
        else:
            task.completed_by = None
            task.completed_at = None

    for field in [
        "title",
        "description",
        "assigned_to",
        "assigned_area",
        "priority",
        "due_date"
    ]:
        if field in data and data[field] is not None:
            setattr(task, field, data[field])

    db.add(
        AuditLog(
            record_id=task.record_id,
            entity_type="task",
            entity_id=task.id,
            action="UPDATE_TASK",
            details=f"Tarea actualizada: {task.title}",
            performed_by=data.get("completed_by")
        )
    )

    db.commit()
    db.refresh(task)

    return task
