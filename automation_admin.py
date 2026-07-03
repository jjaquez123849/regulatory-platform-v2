from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_schema import (
    AutomationRuleCreate,
    AutomationRuleResponse,
    AutomationConditionCreate,
    AutomationActionCreate
)
from app.services.automation_admin_service import (
    create_automation_rule,
    list_automation_rules,
    create_automation_condition,
    list_automation_conditions,
    create_automation_action,
    list_automation_actions
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin - Automation"]
)


@router.post("/automation-rules", response_model=AutomationRuleResponse)
def create_new_automation_rule(
    payload: AutomationRuleCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_automation_rule(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/processes/{process_id}/automation-rules", response_model=list[AutomationRuleResponse])
def read_automation_rules(
    process_id: int,
    db: Session = Depends(get_db)
):
    return list_automation_rules(db, process_id)


@router.post("/automation-conditions")
def create_new_automation_condition(
    payload: AutomationConditionCreate,
    db: Session = Depends(get_db)
):
    try:
        item = create_automation_condition(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "id": item.id,
        "rule_id": item.rule_id,
        "left_value": item.left_value,
        "operator": item.operator,
        "right_value": item.right_value,
        "display_order": item.display_order,
        "is_active": item.is_active
    }


@router.get("/automation-rules/{rule_id}/conditions")
def read_automation_conditions(
    rule_id: int,
    db: Session = Depends(get_db)
):
    items = list_automation_conditions(db, rule_id)

    return [
        {
            "id": item.id,
            "rule_id": item.rule_id,
            "left_value": item.left_value,
            "operator": item.operator,
            "right_value": item.right_value,
            "display_order": item.display_order,
            "is_active": item.is_active
        }
        for item in items
    ]


@router.post("/automation-actions")
def create_new_automation_action(
    payload: AutomationActionCreate,
    db: Session = Depends(get_db)
):
    try:
        item = create_automation_action(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "id": item.id,
        "rule_id": item.rule_id,
        "action_type": item.action_type,
        "action_payload": item.action_payload,
        "display_order": item.display_order,
        "is_active": item.is_active
    }


@router.get("/automation-rules/{rule_id}/actions")
def read_automation_actions(
    rule_id: int,
    db: Session = Depends(get_db)
):
    items = list_automation_actions(db, rule_id)

    return [
        {
            "id": item.id,
            "rule_id": item.rule_id,
            "action_type": item.action_type,
            "action_payload": item.action_payload,
            "display_order": item.display_order,
            "is_active": item.is_active
        }
        for item in items
    ]
