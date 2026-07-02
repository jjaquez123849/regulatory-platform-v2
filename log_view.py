from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.configuration import ProcessField
from app.models.record import Record, RecordValue, RecordPerson, RecordRequestItem
from app.models.workflow import WorkflowState


router = APIRouter(
    prefix="/log",
    tags=["Log View"]
)


def get_record_value_map(db: Session, record_id: int) -> dict:
    values = (
        db.query(RecordValue)
        .filter(RecordValue.record_id == record_id)
        .all()
    )

    result = {}

    for item in values:
        value = (
            item.value_text
            or item.value_number
            or item.value_date
            or item.value_boolean
        )

        result[item.field_id] = value

    return result


def build_log_row(db: Session, record: Record) -> dict:
    fields = (
        db.query(ProcessField)
        .filter(ProcessField.process_id == record.process_id)
        .order_by(ProcessField.display_order.asc(), ProcessField.id.asc())
        .all()
    )

    value_map = get_record_value_map(db, record.id)

    state = None

    if record.current_state_id:
        state = (
            db.query(WorkflowState)
            .filter(WorkflowState.id == record.current_state_id)
            .first()
        )

    people = (
        db.query(RecordPerson)
        .filter(RecordPerson.record_id == record.id)
        .all()
    )

    request_items = (
        db.query(RecordRequestItem)
        .filter(RecordRequestItem.record_id == record.id)
        .all()
    )

    row = {
        "record_id": record.id,
        "process_id": record.process_id,
        "title": record.title,
        "summary": record.summary,
        "state": state.name if state else None,
        "state_id": record.current_state_id,
        "is_complete": record.is_complete,
        "has_pending_items": record.has_pending_items,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "closed_at": record.closed_at,
        "fields": {},
        "people": [],
        "request_items": []
    }

    for field in fields:
        row["fields"][field.name] = {
            "label": field.label,
            "type": field.field_type,
            "value": value_map.get(field.id)
        }

    for person in people:
        row["people"].append({
            "id": person.id,
            "full_name": person.full_name,
            "identification": person.identification,
            "identification_type": person.identification_type,
            "role": person.role
        })

    for item in request_items:
        row["request_items"].append({
            "id": item.id,
            "person_id": item.person_id,
            "request_type": item.request_type,
            "description": item.description,
            "status": item.status,
            "pending_reason": item.pending_reason,
            "response_summary": item.response_summary,
            "is_answered": item.is_answered
        })

    return row


@router.get("/process/{process_id}")
def read_process_log(
    process_id: int,
    db: Session = Depends(get_db)
):
    records = (
        db.query(Record)
        .filter(
            Record.process_id == process_id,
            Record.is_deleted == False
        )
        .order_by(Record.created_at.desc())
        .all()
    )

    return [
        build_log_row(db, record)
        for record in records
    ]


@router.get("/records/{record_id}")
def read_record_log_detail(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(Record)
        .filter(
            Record.id == record_id,
            Record.is_deleted == False
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return build_log_row(db, record)
