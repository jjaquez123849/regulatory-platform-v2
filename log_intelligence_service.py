from sqlalchemy.orm import Session

from app.models.configuration import ProcessField
from app.models.record import Record, RecordValue


def get_log_completion_status(db: Session, record_id: int) -> dict:
    record = (
        db.query(Record)
        .filter(Record.id == record_id, Record.is_deleted == False)
        .first()
    )

    if not record:
        raise ValueError("Registro no encontrado.")

    fields = (
        db.query(ProcessField)
        .filter(
            ProcessField.process_id == record.process_id,
            ProcessField.is_active == True,
        )
        .order_by(ProcessField.display_order.asc())
        .all()
    )

    values = (
        db.query(RecordValue)
        .filter(RecordValue.record_id == record.id)
        .all()
    )

    value_by_field = {item.field_id: item for item in values}

    completed = []
    missing = []

    for field in fields:
        record_value = value_by_field.get(field.id)

        has_value = False
        current_value = None

        if record_value:
            current_value = (
                record_value.value_text
                or record_value.value_number
                or record_value.value_date
                or record_value.value_boolean
            )

            has_value = current_value not in [None, ""]

        item = {
            "field_id": field.id,
            "field_name": field.name,
            "label": field.label,
            "data_type": field.data_type,
            "is_required": field.is_required,
            "value": current_value,
        }

        if has_value:
            completed.append(item)
        elif field.is_required:
            missing.append(item)

    return {
        "record_id": record.id,
        "total_fields": len(fields),
        "completed_count": len(completed),
        "missing_required_count": len(missing),
        "is_complete": len(missing) == 0,
        "completed": completed,
        "missing": missing,
    }
