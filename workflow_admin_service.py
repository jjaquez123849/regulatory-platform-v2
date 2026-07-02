from sqlalchemy.orm import Session

from app.models.workflow import WorkflowState, WorkflowTransition
from app.services.admin_service import get_process


# =========================
# Workflow States
# =========================

def create_workflow_state(db: Session, data: dict) -> WorkflowState:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    existing = (
        db.query(WorkflowState)
        .filter(
            WorkflowState.process_id == data["process_id"],
            WorkflowState.code == data["code"]
        )
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe un estado con el código: {data['code']}")

    if data.get("is_initial"):
        (
            db.query(WorkflowState)
            .filter(WorkflowState.process_id == data["process_id"])
            .update({"is_initial": False})
        )

    state = WorkflowState(
        process_id=data["process_id"],
        code=data["code"],
        name=data["name"],
        display_order=data.get("display_order", 0),
        color=data.get("color"),
        is_initial=data.get("is_initial", False),
        is_final=data.get("is_final", False),
        is_active=data.get("is_active", True)
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


def list_workflow_states(db: Session, process_id: int) -> list[WorkflowState]:
    return (
        db.query(WorkflowState)
        .filter(WorkflowState.process_id == process_id)
        .order_by(WorkflowState.display_order.asc(), WorkflowState.id.asc())
        .all()
    )


def get_workflow_state(db: Session, state_id: int) -> WorkflowState | None:
    return (
        db.query(WorkflowState)
        .filter(WorkflowState.id == state_id)
        .first()
    )


def update_workflow_state(db: Session, state_id: int, data: dict) -> WorkflowState | None:
    state = get_workflow_state(db, state_id)

    if not state:
        return None

    if data.get("is_initial") is True:
        (
            db.query(WorkflowState)
            .filter(WorkflowState.process_id == state.process_id)
            .update({"is_initial": False})
        )

    for key, value in data.items():
        if value is not None:
            setattr(state, key, value)

    db.commit()
    db.refresh(state)

    return state


# =========================
# Workflow Transitions
# =========================

def create_workflow_transition(db: Session, data: dict) -> WorkflowTransition:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    from_state = get_workflow_state(db, data["from_state_id"])
    to_state = get_workflow_state(db, data["to_state_id"])

    if not from_state or not to_state:
        raise ValueError("Estado origen o destino no encontrado.")

    if from_state.process_id != data["process_id"] or to_state.process_id != data["process_id"]:
        raise ValueError("Los estados deben pertenecer al mismo proceso.")

    existing = (
        db.query(WorkflowTransition)
        .filter(
            WorkflowTransition.process_id == data["process_id"],
            WorkflowTransition.code == data["code"]
        )
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe una transición con el código: {data['code']}")

    transition = WorkflowTransition(
        process_id=data["process_id"],
        code=data["code"],
        name=data["name"],
        from_state_id=data["from_state_id"],
        to_state_id=data["to_state_id"],
        requires_comment=data.get("requires_comment", False),
        requires_checklist_completed=data.get("requires_checklist_completed", False),
        is_active=data.get("is_active", True)
    )

    db.add(transition)
    db.commit()
    db.refresh(transition)

    return transition


def list_workflow_transitions(db: Session, process_id: int) -> list[WorkflowTransition]:
    return (
        db.query(WorkflowTransition)
        .filter(WorkflowTransition.process_id == process_id)
        .order_by(WorkflowTransition.id.asc())
        .all()
    )


def get_workflow_transition(db: Session, transition_id: int) -> WorkflowTransition | None:
    return (
        db.query(WorkflowTransition)
        .filter(WorkflowTransition.id == transition_id)
        .first()
    )


def update_workflow_transition(
    db: Session,
    transition_id: int,
    data: dict
) -> WorkflowTransition | None:
    transition = get_workflow_transition(db, transition_id)

    if not transition:
        return None

    if data.get("from_state_id") is not None:
        from_state = get_workflow_state(db, data["from_state_id"])
        if not from_state or from_state.process_id != transition.process_id:
            raise ValueError("Estado origen inválido.")

    if data.get("to_state_id") is not None:
        to_state = get_workflow_state(db, data["to_state_id"])
        if not to_state or to_state.process_id != transition.process_id:
            raise ValueError("Estado destino inválido.")

    for key, value in data.items():
        if value is not None:
            setattr(transition, key, value)

    db.commit()
    db.refresh(transition)

    return transition
