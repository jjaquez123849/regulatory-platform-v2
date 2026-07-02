from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.record import Record, RecordValue
from app.models.configuration import ProcessField
from app.models.workflow import WorkflowState
from app.models.audit import AuditLog
from app.services.admin_service import get_process


def get_initial_state_id(db: Session, process_id: int) -> int | None:
    state = (
        db.query(WorkflowState)
        .filter(
            WorkflowState.process_id == process_id,
            WorkflowState.is_initial == True,
            WorkflowState.is_active == True
        )
        .first()
    )

    if state:
        return state.id

    state = (
        db.query(WorkflowState)
        .filter(
            WorkflowState.process_id == process_id,
            WorkflowState.is_active == True
        )
        .order_by(WorkflowState.display_order.asc(), WorkflowState.id.asc())
        .first()
    )

    return state.id if state else None


def get_process_fields(db: Session, process_id: int) -> list[ProcessField]:
    return (
        db.query(ProcessField)
        .filter(ProcessField.process_id == process_id)
        .order_by(ProcessField.display_order.asc(), ProcessField.id.asc())
        .all()
    )


def validate_record_values(db: Session, process_id: int, values: dict[str, Any]) -> list[str]:
    errors = []
    fields = get_process_fields(db, process_id)

    fields_by_name = {field.name: field for field in fields}

    for field in fields:
        if field.is_required:
            value = values.get(field.name)
            if value is None or str(value).strip() == "":
                errors.append(f"El campo '{field.label}' es obligatorio.")

    for field_name in values.keys():
        if field_name not in fields_by_name:
            errors.append(f"El campo '{field_name}' no existe en este proceso.")

    return errors


def create_record_value(
    record_id: int,
    field: ProcessField,
    value: Any
) -> RecordValue:
    record_value = RecordValue(
        record_id=record_id,
        field_id=field.id,
        updated_at=datetime.utcnow()
    )

    if field.field_type in ["number", "currency"]:
        record_value.value_number = str(value) if value is not None else None
    elif field.field_type in ["date", "datetime"]:
        record_value.value_date = str(value) if value is not None else None
    elif field.field_type == "boolean":
        record_value.value_boolean = bool(value) if value is not None else None
    else:
        record_value.value_text = str(value) if value is not None else None

    return record_value


def get_value_from_record_value(item: RecordValue, field_type: str):
    if field_type in ["number", "currency"]:
        return item.value_number
    if field_type in ["date", "datetime"]:
        return item.value_date
    if field_type == "boolean":
        return item.value_boolean
    return item.value_text


def create_record(db: Session, data: dict) -> Record:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    errors = validate_record_values(
        db=db,
        process_id=data["process_id"],
        values=data.get("values", {})
    )

    if errors:
        raise ValueError(" | ".join(errors))

    initial_state_id = get_initial_state_id(db, data["process_id"])

    record = Record(
        process_id=data["process_id"],
        current_state_id=initial_state_id,
        title=data.get("title"),
        summary=data.get("summary"),
        source_channel=data.get("source_channel"),
        created_by=data.get("created_by"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(record)
    db.flush()

    fields = get_process_fields(db, data["process_id"])
    fields_by_name = {field.name: field for field in fields}

    for field_name, value in data.get("values", {}).items():
        field = fields_by_name[field_name]
        db.add(create_record_value(record.id, field, value))

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="record",
            entity_id=record.id,
            action="CREATE_RECORD",
            details="Registro creado",
            performed_by=data.get("created_by")
        )
    )

    db.commit()
    db.refresh(record)

    return record


def list_records(db: Session, process_id: int | None = None) -> list[Record]:
    query = db.query(Record).filter(Record.is_deleted == False)

    if process_id:
        query = query.filter(Record.process_id == process_id)

    return query.order_by(Record.created_at.desc()).all()


def get_record(db: Session, record_id: int) -> Record | None:
    return (
        db.query(Record)
        .filter(
            Record.id == record_id,
            Record.is_deleted == False
        )
        .first()
    )


def record_to_response(db: Session, record: Record) -> dict:
    fields = get_process_fields(db, record.process_id)
    values = (
        db.query(RecordValue)
        .filter(RecordValue.record_id == record.id)
        .all()
    )

    values_by_field_id = {item.field_id: item for item in values}

    response_values = []

    for field in fields:
        existing_value = values_by_field_id.get(field.id)

        response_values.append(
            {
                "field_id": field.id,
                "field_name": field.name,
                "field_label": field.label,
                "field_type": field.field_type,
                "value": get_value_from_record_value(existing_value, field.field_type)
                if existing_value else None
            }
        )

    return {
        "id": record.id,
        "process_id": record.process_id,
        "current_state_id": record.current_state_id,
        "title": record.title,
        "summary": record.summary,
        "source_channel": record.source_channel,
        "is_complete": record.is_complete,
        "has_pending_items": record.has_pending_items,
        "values": response_values
    }


def update_record(db: Session, record_id: int, data: dict) -> Record | None:
    record = get_record(db, record_id)

    if not record:
        return None

    for field in ["title", "summary", "source_channel", "is_complete", "has_pending_items"]:
        if field in data and data[field] is not None:
            setattr(record, field, data[field])

    if data.get("values") is not None:
        errors = validate_record_values(
            db=db,
            process_id=record.process_id,
            values=data["values"]
        )

        if errors:
            raise ValueError(" | ".join(errors))

        fields = get_process_fields(db, record.process_id)
        fields_by_name = {field.name: field for field in fields}

        existing_values = (
            db.query(RecordValue)
            .filter(RecordValue.record_id == record.id)
            .all()
        )

        existing_by_field_id = {item.field_id: item for item in existing_values}

        for field_name, value in data["values"].items():
            field = fields_by_name[field_name]
            existing = existing_by_field_id.get(field.id)

            if existing:
                if field.field_type in ["number", "currency"]:
                    existing.value_number = str(value) if value is not None else None
                elif field.field_type in ["date", "datetime"]:
                    existing.value_date = str(value) if value is not None else None
                elif field.field_type == "boolean":
                    existing.value_boolean = bool(value) if value is not None else None
                else:
                    existing.value_text = str(value) if value is not None else None

                existing.updated_at = datetime.utcnow()
            else:
                db.add(create_record_value(record.id, field, value))

    record.updated_at = datetime.utcnow()

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="record",
            entity_id=record.id,
            action="UPDATE_RECORD",
            details="Registro actualizado"
        )
    )

    db.commit()
    db.refresh(record)

    return record
