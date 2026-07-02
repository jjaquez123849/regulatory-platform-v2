from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.workflow_schema import WorkflowTransitionRequest
from app.services.workflow_service import (
    get_available_transitions,
    apply_transition,
    get_workflow_history
)
from app.services.record_service import record_to_response


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"]
)


@router.get("/records/{record_id}/available-transitions")
def read_available_transitions(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:
        transitions = get_available_transitions(db, record_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    return [
        {
            "id": item.id,
            "process_id": item.process_id,
            "code": item.code,
            "name": item.name,
            "from_state_id": item.from_state_id,
            "to_state_id": item.to_state_id,
            "requires_comment": item.requires_comment,
            "requires_checklist_completed": item.requires_checklist_completed,
            "is_active": item.is_active
        }
        for item in transitions
    ]


@router.post("/records/{record_id}/transition")
def apply_record_transition(
    record_id: int,
    payload: WorkflowTransitionRequest,
    db: Session = Depends(get_db)
):
    try:
        record = apply_transition(
            db=db,
            record_id=record_id,
            transition_id=payload.transition_id,
            comment=payload.comment,
            performed_by=payload.performed_by
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return record_to_response(db, record)


@router.get("/records/{record_id}/history")
def read_workflow_history(
    record_id: int,
    db: Session = Depends(get_db)
):
    history = get_workflow_history(db, record_id)

    return [
        {
            "id": item.id,
            "record_id": item.record_id,
            "transition_id": item.transition_id,
            "from_state_id": item.from_state_id,
            "to_state_id": item.to_state_id,
            "comment": item.comment,
            "performed_by": item.performed_by,
            "performed_at": item.performed_at
        }
        for item in history
    ]
