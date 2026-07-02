from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_schema import (
    WorkflowStateCreate,
    WorkflowStateUpdate,
    WorkflowStateResponse,
    WorkflowTransitionCreate,
    WorkflowTransitionUpdate,
    WorkflowTransitionResponse
)
from app.services.workflow_admin_service import (
    create_workflow_state,
    list_workflow_states,
    get_workflow_state,
    update_workflow_state,
    create_workflow_transition,
    list_workflow_transitions,
    get_workflow_transition,
    update_workflow_transition
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin - Workflow"]
)


# =========================
# Workflow States
# =========================

@router.post("/workflow-states", response_model=WorkflowStateResponse)
def create_new_workflow_state(
    payload: WorkflowStateCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_workflow_state(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get(
    "/processes/{process_id}/workflow-states",
    response_model=list[WorkflowStateResponse]
)
def read_workflow_states(
    process_id: int,
    db: Session = Depends(get_db)
):
    return list_workflow_states(
        db=db,
        process_id=process_id
    )


@router.get("/workflow-states/{state_id}", response_model=WorkflowStateResponse)
def read_workflow_state(
    state_id: int,
    db: Session = Depends(get_db)
):
    state = get_workflow_state(db, state_id)

    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    return state


@router.put("/workflow-states/{state_id}", response_model=WorkflowStateResponse)
def update_existing_workflow_state(
    state_id: int,
    payload: WorkflowStateUpdate,
    db: Session = Depends(get_db)
):
    try:
        state = update_workflow_state(
            db=db,
            state_id=state_id,
            data=payload.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not state:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    return state


# =========================
# Workflow Transitions
# =========================

@router.post("/workflow-transitions", response_model=WorkflowTransitionResponse)
def create_new_workflow_transition(
    payload: WorkflowTransitionCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_workflow_transition(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get(
    "/processes/{process_id}/workflow-transitions",
    response_model=list[WorkflowTransitionResponse]
)
def read_workflow_transitions(
    process_id: int,
    db: Session = Depends(get_db)
):
    return list_workflow_transitions(
        db=db,
        process_id=process_id
    )


@router.get("/workflow-transitions/{transition_id}", response_model=WorkflowTransitionResponse)
def read_workflow_transition(
    transition_id: int,
    db: Session = Depends(get_db)
):
    transition = get_workflow_transition(db, transition_id)

    if not transition:
        raise HTTPException(status_code=404, detail="Transición no encontrada")

    return transition


@router.put("/workflow-transitions/{transition_id}", response_model=WorkflowTransitionResponse)
def update_existing_workflow_transition(
    transition_id: int,
    payload: WorkflowTransitionUpdate,
    db: Session = Depends(get_db)
):
    try:
        transition = update_workflow_transition(
            db=db,
            transition_id=transition_id,
            data=payload.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not transition:
        raise HTTPException(status_code=404, detail="Transición no encontrada")

    return transition
