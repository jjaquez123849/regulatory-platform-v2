from datetime import datetime, date

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.record import Record, RecordValue


def update_log_values(
    db: Session,
    record_id: int,
    values: list[dict],
    updated_by: str | None = None,
) -> dict:
    record = (
        db.query(Record)
        .filter(
            Record.id == record_id,
            Record.is_deleted == False,
        )
        .first()
    )

    if not record:
        raise ValueError("Registro no encontrado.")

    updated_count = 0

    for item in values:
        field_id = item["field_id"]
        raw_value = item.get("value")

        record_value = (
            db.query(RecordValue)
            .filter(
                RecordValue.record_id == record_id,
                RecordValue.field_id == field_id,
            )
            .first()
        )

        if not record_value:
            record_value = RecordValue(
                record_id=record_id,
                field_id=field_id,
            )
            db.add(record_value)

        record_value.value_text = None
        record_value.value_number = None
        record_value.value_date = None
        record_value.value_boolean = None

        if isinstance(raw_value, bool):
            record_value.value_boolean = raw_value
        elif isinstance(raw_value, int) or isinstance(raw_value, float):
            record_value.value_number = raw_value
        elif isinstance(raw_value, date):
            record_value.value_date = raw_value
        elif raw_value is not None:
            record_value.value_text = str(raw_value)

        updated_count += 1

    record.updated_at = datetime.utcnow()

    db.add(
        AuditLog(
            record_id=record_id,
            entity_type="record",
            entity_id=record_id,
            action="UPDATE_LOG_VALUES",
            details=f"Valores actualizados: {updated_count}",
            performed_by=updated_by,
        )
    )

    db.commit()

    return {
        "status": "updated",
        "record_id": record_id,
        "updated_count": updated_count,
    }
