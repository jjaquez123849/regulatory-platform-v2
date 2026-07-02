from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task,
    list_tasks,
    get_task,
    update_task
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def task_to_dict(task):
    return {
        "id": task.id,
        "record_id": task.record_id,
        "title": task.title,
        "description": task.description,
        "assigned_to": task.assigned_to,
        "assigned_area": task.assigned_area,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "created_by": task.created_by,
        "created_at": task.created_at,
        "completed_by": task.completed_by,
        "completed_at": task.completed_at
    }


@router.post("/")
def create_new_task(
    payload: TaskCreate,
    db: Session = Depends(get_db)
):
    try:
        task = create_task(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return task_to_dict(task)


@router.get("/")
def read_tasks(
    record_id: int | None = Query(None),
    status: str | None = Query(None),
    assigned_to: str | None = Query(None),
    assigned_area: str | None = Query(None),
    db: Session = Depends(get_db)
):
    tasks = list_tasks(
        db=db,
        record_id=record_id,
        status=status,
        assigned_to=assigned_to,
        assigned_area=assigned_area
    )

    return [task_to_dict(task) for task in tasks]


@router.get("/{task_id}")
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return task_to_dict(task)


@router.put("/{task_id}")
def update_existing_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):
    try:
        task = update_task(
            db=db,
            task_id=task_id,
            data=payload.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return task_to_dict(task)
