from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document import DocumentExtractionResult
from app.models.record import RecordValue, RecordPerson, RecordRequestItem
from app.models.configuration import ProcessField
from app.models.audit import AuditLog


def get_process_field_by_name(
    db: Session,
    process_id: int,
    field_name: str
) -> ProcessField | None:
    return (
        db.query(ProcessField)
        .filter(
            ProcessField.process_id == process_id,
            ProcessField.name == field_name
        )
        .first()
    )


def apply_record_field_value(
    db: Session,
    record_id: int,
    process_id: int,
    field_name: str,
    value: str
):
    field = get_process_field_by_name(
        db=db,
        process_id=process_id,
        field_name=field_name
    )

    if not field:
        return None

    existing = (
        db.query(RecordValue)
        .filter(
            RecordValue.record_id == record_id,
            RecordValue.field_id == field.id
        )
        .first()
    )

    if not existing:
        existing = RecordValue(
            record_id=record_id,
            field_id=field.id
        )
        db.add(existing)

    if field.field_type in ["number", "currency"]:
        existing.value_number = value
    elif field.field_type in ["date", "datetime"]:
        existing.value_date = value
    elif field.field_type == "boolean":
        existing.value_boolean = str(value).strip().lower() in ["true", "1", "yes", "si", "sí"]
    else:
        existing.value_text = value

    existing.updated_at = datetime.utcnow()

    return existing


def apply_person_value(
    db: Session,
    record_id: int,
    field_name: str,
    value: str
):
    person = (
        db.query(RecordPerson)
        .filter(RecordPerson.record_id == record_id)
        .order_by(RecordPerson.id.desc())
        .first()
    )

    if not person:
        person = RecordPerson(
            record_id=record_id,
            full_name="Pendiente identificar",
            created_at=datetime.utcnow()
        )
        db.add(person)
        db.flush()

    if field_name == "full_name":
        person.full_name = value
    elif field_name == "identification":
        person.identification = value
    elif field_name == "identification_type":
        person.identification_type = value
    elif field_name == "role":
        person.role = value
    else:
        person.notes = f"{field_name}: {value}"

    return person


def apply_request_item_value(
    db: Session,
    record_id: int,
    field_name: str,
    value: str
):
    item = (
        db.query(RecordRequestItem)
        .filter(RecordRequestItem.record_id == record_id)
        .order_by(RecordRequestItem.id.desc())
        .first()
    )

    if not item:
        item = RecordRequestItem(
            record_id=record_id,
            request_type="pendiente_clasificar",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(item)
        db.flush()

    if field_name == "request_type":
        item.request_type = value
    elif field_name == "description":
        item.description = value
    elif field_name == "status":
        item.status = value
    elif field_name == "pending_reason":
        item.pending_reason = value
    elif field_name == "response_summary":
        item.response_summary = value
    elif field_name == "is_answered":
        item.is_answered = str(value).strip().lower() in ["true", "1", "yes", "si", "sí"]
    else:
        item.description = f"{item.description or ''}\n{field_name}: {value}".strip()

    item.updated_at = datetime.utcnow()

    return item


def apply_extraction_results(
    db: Session,
    document_id: int,
    performed_by: str | None = None
) -> dict:
    results = (
        db.query(DocumentExtractionResult)
        .filter(
            DocumentExtractionResult.document_id == document_id,
            DocumentExtractionResult.status == "proposed"
        )
        .all()
    )

    if not results:
        return {
            "status": "no_results",
            "message": "No hay resultados propuestos para aplicar.",
            "applied_count": 0
        }

    applied_count = 0
    record_id = results[0].record_id

    if not record_id:
        raise ValueError("Los resultados no están asociados a un registro.")

    from app.services.record_service import get_record

    record = get_record(db, record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    for result in results:
        value = result.normalized_value or result.extracted_value

        if not value:
            continue

        if result.target_entity == "record":
            apply_record_field_value(
                db=db,
                record_id=record.id,
                process_id=record.process_id,
                field_name=result.target_field,
                value=value
            )

        elif result.target_entity == "person":
            apply_person_value(
                db=db,
                record_id=record.id,
                field_name=result.target_field,
                value=value
            )

        elif result.target_entity == "request_item":
            apply_request_item_value(
                db=db,
                record_id=record.id,
                field_name=result.target_field,
                value=value
            )

        result.status = "applied"
        result.reviewed_by = performed_by
        result.reviewed_at = datetime.utcnow()

        applied_count += 1

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="document",
            entity_id=document_id,
            action="APPLY_EXTRACTION_RESULTS",
            details=f"Resultados aplicados: {applied_count}",
            performed_by=performed_by
        )
    )

    db.commit()

    return {
        "status": "applied",
        "document_id": document_id,
        "record_id": record.id,
        "applied_count": applied_count
    }
