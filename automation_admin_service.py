from datetime import datetime
from sqlalchemy.orm import Session

from app.models.automation import AutomationRule, AutomationCondition, AutomationAction
from app.services.admin_service import get_process


def create_automation_rule(db: Session, data: dict) -> AutomationRule:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    existing = (
        db.query(AutomationRule)
        .filter(
            AutomationRule.process_id == data["process_id"],
            AutomationRule.code == data["code"]
        )
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe una automatización con el código: {data['code']}")

    rule = AutomationRule(
        process_id=data["process_id"],
        code=data["code"],
        name=data["name"],
        description=data.get("description"),
        trigger_event=data["trigger_event"],
        is_active=data.get("is_active", True),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


def list_automation_rules(db: Session, process_id: int) -> list[AutomationRule]:
    return (
        db.query(AutomationRule)
        .filter(AutomationRule.process_id == process_id)
        .order_by(AutomationRule.id.asc())
        .all()
    )


def get_automation_rule(db: Session, rule_id: int) -> AutomationRule | None:
    return db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()


def create_automation_condition(db: Session, data: dict) -> AutomationCondition:
    rule = get_automation_rule(db, data["rule_id"])

    if not rule:
        raise ValueError("Regla de automatización no encontrada.")

    condition = AutomationCondition(
        rule_id=data["rule_id"],
        left_value=data["left_value"],
        operator=data["operator"],
        right_value=data.get("right_value"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True)
    )

    db.add(condition)
    db.commit()
    db.refresh(condition)

    return condition


def list_automation_conditions(db: Session, rule_id: int) -> list[AutomationCondition]:
    return (
        db.query(AutomationCondition)
        .filter(AutomationCondition.rule_id == rule_id)
        .order_by(AutomationCondition.display_order.asc(), AutomationCondition.id.asc())
        .all()
    )


def create_automation_action(db: Session, data: dict) -> AutomationAction:
    rule = get_automation_rule(db, data["rule_id"])

    if not rule:
        raise ValueError("Regla de automatización no encontrada.")

    action = AutomationAction(
        rule_id=data["rule_id"],
        action_type=data["action_type"],
        action_payload=data.get("action_payload"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True)
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return action


def list_automation_actions(db: Session, rule_id: int) -> list[AutomationAction]:
    return (
        db.query(AutomationAction)
        .filter(AutomationAction.rule_id == rule_id)
        .order_by(AutomationAction.display_order.asc(), AutomationAction.id.asc())
        .all()
    )
