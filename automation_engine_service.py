import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.automation_actions import AutomationAction
from app.models.automation import AutomationRule, AutomationCondition, AutomationAction as AutomationActionModel
from app.models.audit import AuditLog


def get_context_value(context: dict, path: str):
    """
    Permite leer valores tipo:
    record.id
    document.file_extension
    event.name
    """
    parts = path.split(".")
    value = context

    for part in parts:
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None

    return value


def evaluate_condition(condition: AutomationCondition, context: dict) -> bool:
    left = get_context_value(context, condition.left_value)
    right = condition.right_value
    operator = condition.operator

    if operator == "equals":
        return str(left) == str(right)

    if operator == "not_equals":
        return str(left) != str(right)

    if operator == "contains":
        return str(right).lower() in str(left or "").lower()

    if operator == "not_contains":
        return str(right).lower() not in str(left or "").lower()

    if operator == "is_empty":
        return left is None or str(left).strip() == ""

    if operator == "is_not_empty":
        return left is not None and str(left).strip() != ""

    if operator == "starts_with":
        return str(left or "").startswith(str(right))

    if operator == "ends_with":
        return str(left or "").endswith(str(right))

    if operator == "in_list":
        values = [item.strip() for item in str(right or "").split(",")]
        return str(left) in values

    if operator == "not_in_list":
        values = [item.strip() for item in str(right or "").split(",")]
        return str(left) not in values

    return False


def rule_conditions_pass(db: Session, rule: AutomationRule, context: dict) -> bool:
    conditions = (
        db.query(AutomationCondition)
        .filter(
            AutomationCondition.rule_id == rule.id,
            AutomationCondition.is_active == True
        )
        .order_by(AutomationCondition.display_order.asc())
        .all()
    )

    if not conditions:
        return True

    return all(evaluate_condition(condition, context) for condition in conditions)


def parse_payload(raw_payload: str | None) -> dict:
    if not raw_payload:
        return {}

    try:
        return json.loads(raw_payload)
    except Exception:
        return {}


def execute_action(
    db: Session,
    action: AutomationActionModel,
    context: dict
) -> dict:
    payload = parse_payload(action.action_payload)

    if action.action_type == AutomationAction.CREATE_TASK:
        from app.services.task_service import create_task

        record_id = payload.get("record_id") or get_context_value(context, "record.id")

        task = create_task(
            db=db,
            data={
                "record_id": record_id,
                "title": payload.get("title", "Tarea automática"),
                "description": payload.get("description"),
                "assigned_to": payload.get("assigned_to"),
                "assigned_area": payload.get("assigned_area"),
                "priority": payload.get("priority", "medium"),
                "due_date": None,
                "created_by": payload.get("created_by", "automation")
            }
        )

        return {
            "action": action.action_type,
            "status": "executed",
            "task_id": task.id
        }

    if action.action_type == AutomationAction.EXECUTE_EXTRACTION:
        from app.services.document_processing_service import process_document

        document_id = payload.get("document_id") or get_context_value(context, "document.id")

        result = process_document(
            db=db,
            document_id=document_id
        )

        return {
            "action": action.action_type,
            "status": "executed",
            "result": result
        }

    if action.action_type == AutomationAction.APPLY_EXTRACTION:
        from app.services.extraction_apply_service import apply_extraction_results

        document_id = payload.get("document_id") or get_context_value(context, "document.id")

        result = apply_extraction_results(
            db=db,
            document_id=document_id,
            performed_by="automation"
        )

        return {
            "action": action.action_type,
            "status": "executed",
            "result": result
        }

    if action.action_type == AutomationAction.EXECUTE_QUALITY:
        from app.services.quality_service import run_quality_review

        record_id = payload.get("record_id") or get_context_value(context, "record.id")
        document_id = payload.get("document_id") or get_context_value(context, "document.id")

        result = run_quality_review(
            db=db,
            record_id=record_id,
            document_id=document_id,
            reviewed_by="automation"
        )

        return {
            "action": action.action_type,
            "status": "executed",
            "quality_review_id": result.id
        }

    if action.action_type == AutomationAction.CHANGE_STATE:
        from app.models.record import Record
        from app.models.workflow import WorkflowHistory, WorkflowState

        record_id = payload.get("record_id") or get_context_value(context, "record.id")
        to_state_id = payload.get("to_state_id")

        if not record_id or not to_state_id:
            return {
                "action": action.action_type,
                "status": "error",
                "reason": "Falta record_id o to_state_id"
            }

        record = db.query(Record).filter(Record.id == record_id).first()

        if not record:
            return {
                "action": action.action_type,
                "status": "error",
                "reason": "Registro no encontrado"
            }

        target_state = (
            db.query(WorkflowState)
            .filter(
                WorkflowState.id == int(to_state_id),
                WorkflowState.process_id == record.process_id
            )
            .first()
        )

        if not target_state:
            return {
                "action": action.action_type,
                "status": "error",
                "reason": "Estado destino no válido"
            }

        previous_state_id = record.current_state_id
        record.current_state_id = target_state.id
        record.updated_at = datetime.utcnow()

        if target_state.is_final:
            record.closed_at = datetime.utcnow()
            record.is_complete = True

        db.add(
            WorkflowHistory(
                record_id=record.id,
                transition_id=None,
                from_state_id=previous_state_id,
                to_state_id=target_state.id,
                comment="Cambio de estado ejecutado por automatización",
                performed_by="automation",
                performed_at=datetime.utcnow()
            )
        )

        return {
            "action": action.action_type,
            "status": "executed",
            "record_id": record.id,
            "from_state_id": previous_state_id,
            "to_state_id": target_state.id
        }

    return {
        "action": action.action_type,
        "status": "skipped",
        "reason": "Acción aún no implementada"
    }


def run_automation_event(
    db: Session,
    process_id: int,
    trigger_event: str,
    context: dict
) -> dict:
    rules = (
        db.query(AutomationRule)
        .filter(
            AutomationRule.process_id == process_id,
            AutomationRule.trigger_event == trigger_event,
            AutomationRule.is_active == True
        )
        .order_by(AutomationRule.id.asc())
        .all()
    )

    executed_rules = []

    for rule in rules:
        if not rule_conditions_pass(db, rule, context):
            executed_rules.append({
                "rule_id": rule.id,
                "rule_code": rule.code,
                "status": "conditions_not_met"
            })
            continue

        actions = (
            db.query(AutomationActionModel)
            .filter(
                AutomationActionModel.rule_id == rule.id,
                AutomationActionModel.is_active == True
            )
            .order_by(AutomationActionModel.display_order.asc())
            .all()
        )

        action_results = []

        for action in actions:
            action_results.append(
                execute_action(
                    db=db,
                    action=action,
                    context=context
                )
            )

        executed_rules.append({
            "rule_id": rule.id,
            "rule_code": rule.code,
            "status": "executed",
            "actions": action_results
        })

    record_id = get_context_value(context, "record.id")

    db.add(
        AuditLog(
            record_id=record_id,
            entity_type="automation",
            entity_id=None,
            action="RUN_AUTOMATION_EVENT",
            details=str({
                "trigger_event": trigger_event,
                "rules_found": len(rules),
                "executed_rules": executed_rules
            }),
            performed_by="automation"
        )
    )

    db.commit()

    return {
        "trigger_event": trigger_event,
        "rules_found": len(rules),
        "executed_rules": executed_rules,
        "executed_at": datetime.utcnow()
    }
