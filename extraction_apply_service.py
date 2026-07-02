from datetime import datetime
from collections import defaultdict

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


def get_or_create_person_from_group(
    db: Session,
    record_id: int,
    group_values: dict
) -> RecordPerson:
    full_name = group_values.get("person.full_name")
    identification = group_values.get("person.identification")

    query = db.query(RecordPerson).filter(RecordPerson.record_id == record_id)

    if identification:
        existing = query.filter(RecordPerson.identification == identification).first()
        if existing:
            return existing

    if full_name:
        existing = query.filter(RecordPerson.full_name == full_name).first()
        if existing:
            return existing

    person = RecordPerson(
        record_id=record_id,
        full_name=full_name or "Pendiente identificar",
        identification=identification,
        identification_type=group_values.get("person.identification_type"),
        role=group_values.get("person.role"),
        notes=group_values.get("person.notes"),
        source="document_extraction",
        confidence_score="1.0",
        created_at=datetime.utcnow()
    )

    db.add(person)
    db.flush()

    return person


def get_or_create_request_item_from_group(
    db: Session,
    record_id: int,
    person_id: int | None,
    group_values: dict
) -> RecordRequestItem:
    request_type = (
        group_values.get("request_item.request_type")
        or group_values.get("request_item.status")
        or "pendiente_clasificar"
    )

    description_parts = []

    for key, value in group_values.items():
        if key.startswith("request_item.") and key not in [
            "request_item.request_type",
            "request_item.status",
            "request_item.pending_reason",
            "request_item.response_summary",
            "request_item.is_answered"
        ]:
            description_parts.append(f"{key.replace('request_item.', '')}: {value}")

    existing = None

    if person_id:
        existing = (
            db.query(RecordRequestItem)
            .filter(
                RecordRequestItem.record_id == record_id,
                RecordRequestItem.person_id == person_id,
                RecordRequestItem.request_type == request_type
            )
            .first()
        )

    if existing:
        item = existing
    else:
        item = RecordRequestItem(
            record_id=record_id,
            person_id=person_id,
            request_type=request_type,
            created_at=datetime.utcnow()
        )
        db.add(item)
        db.flush()

    if description_parts:
        item.description = "\n".join(description_parts)

    if group_values.get("request_item.status"):
        item.status = group_values.get("request_item.status")

    if group_values.get("request_item.pending_reason"):
        item.pending_reason = group_values.get("request_item.pending_reason")

    if group_values.get("request_item.response_summary"):
        item.response_summary = group_values.get("request_item.response_summary")

    if group_values.get("request_item.is_answered") is not None:
        item.is_answered = str(group_values.get("request_item.is_answered")).strip().lower() in [
            "true", "1", "yes", "si", "sí", "respondido", "completo"
        ]

    item.updated_at = datetime.utcnow()

    return item


def apply_grouped_results(
    db: Session,
    record,
    grouped_results: dict
) -> int:
    applied_count = 0

    for group_key, results in grouped_results.items():
        group_values = {}

        for result in results:
            value = result.normalized_value or result.extracted_value

            if not value:
                continue

            key = f"{result.target_entity}.{result.target_field}"
            group_values[key] = value

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

                result.status = "applied"
                result.reviewed_at = datetime.utcnow()
                applied_count += 1

        person = None

        if any(key.startswith("person.") for key in group_values.keys()):
            person = get_or_create_person_from_group(
                db=db,
                record_id=record.id,
                group_values=group_values
            )

        if any(key.startswith("request_item.") for key in group_values.keys()):
            get_or_create_request_item_from_group(
                db=db,
                record_id=record.id,
                person_id=person.id if person else None,
                group_values=group_values
            )

        for result in results:
            if result.target_entity in ["person", "request_item"]:
                result.status = "applied"
                result.reviewed_at = datetime.utcnow()
                applied_count += 1

    return applied_count


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

    record_id = results[0].record_id

    if not record_id:
        raise ValueError("Los resultados no están asociados a un registro.")

    from app.services.record_service import get_record

    record = get_record(db, record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    grouped_results = defaultdict(list)

    for result in results:
        group_key = result.source_group_key or f"result:{result.id}"
        grouped_results[group_key].append(result)

    applied_count = apply_grouped_results(
        db=db,
        record=record,
        grouped_results=grouped_results
    )

    for result in results:
        if result.status == "applied":
            result.reviewed_by = performed_by

    db.add(
        AuditLog(
            record_id=record.id,
            entity_type="document",
            entity_id=document_id,
            action="APPLY_EXTRACTION_RESULTS",
            details=f"Resultados aplicados por grupos: {applied_count}",
            performed_by=performed_by
        )
    )

    db.commit()

    return {
        "status": "applied",
        "document_id": document_id,
        "record_id": record.id,
        "groups_count": len(grouped_results),
        "applied_count": applied_count
    }
