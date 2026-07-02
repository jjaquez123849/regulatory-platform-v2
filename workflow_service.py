from datetime import datetime

from sqlalchemy.orm import Session

from app.models.record import Record
from app.models.workflow import WorkflowTransition, WorkflowHistory, WorkflowState
from app.models.audit import AuditLog
from app.services.record_service import get_record


def get_available_transitions(db: Session, record_id: int) -> list[WorkflowTransition]:
    record = get_record(db, record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    if not record.current_state_id:
        return []

    return (
        db.query(WorkflowTransition)
        .filter(
            WorkflowTransition.process_id == record.process_id,
            WorkflowTransition.from_state_id == record.current_state_id,
            WorkflowTransition.is_active == True
        )
        .order_by(WorkflowTransition.id.asc())
        .all()
    )


def get_state(db: Session, state_id: int) -> WorkflowState | None:
    return (
        db.query(WorkflowState)
        .filter(WorkflowState.id == state_id)
        .first()
    )


def apply_transition(
    db: Session,
    record_id: int,
    transition_id: int,
    comment: str | None = None,
    performed_by: str | None = None
) -> Record:
    record = get_record(db, record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    transition = (
        db.query(WorkflowTransition)
        .filter(
            WorkflowTransition.id == transition_id,
            WorkflowTransition.process_id == record.process_id,
            WorkflowTransition.is_active == True
        )
        .first()
    )

    if not transition:
        raise ValueError("Transición no encontrada o inactiva.")

    if transition.from_state_id != record.current_state_id:
        raise ValueError("La transición no está permitida desde el estado actual.")

    if transition.requires_comment and not comment:
        raise ValueError("Esta transición requiere comentario.")

    previous_state_id = record.current_state_id
    new_state_id = transition.to_state_id

    record.current_state_id = new_state_id
    record.updated_at = datetime.utcnow()

    new_state = get_state(db, new_state_id)

    if new_state and new_state.is_final:
        record.closed_at = datetime.utcnow()
        record.is_complete = True

    db.add(
        WorkflowHistory(
            record_id=record.id,
            transition_id=transition.id,
            from_state_id=previous_state_id,
            to_state_id=new_state_id,
            comment=comment,
            performed_by=performed_by,
            performed_at=datetime.utcnow()
        )
    )

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="record",
            entity_id=record.id,
            action="WORKFLOW_TRANSITION",
            details=f"Transición aplicada: {transition.name}",
            performed_by=performed_by
        )
    )

    db.commit()
    db.refresh(record)

    return record


def get_workflow_history(db: Session, record_id: int) -> list[WorkflowHistory]:
    return (
        db.query(WorkflowHistory)
        .filter(WorkflowHistory.record_id == record_id)
        .order_by(WorkflowHistory.performed_at.desc())
        .all()
    )
