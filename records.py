from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.record_schema import RecordCreate, RecordUpdate
from app.services.record_service import (
    create_record,
    list_records,
    get_record,
    update_record,
    record_to_response
)


router = APIRouter(
    prefix="/records",
    tags=["Records"]
)


@router.post("/")
def create_new_record(
    payload: RecordCreate,
    db: Session = Depends(get_db)
):
    try:
        record = create_record(
            db=db,
            data=payload.model_dump()
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return record_to_response(db, record)


@router.get("/")
def read_records(
    process_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    records = list_records(
        db=db,
        process_id=process_id
    )

    return [
        record_to_response(db, record)
        for record in records
    ]


@router.get("/{record_id}")
def read_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = get_record(
        db=db,
        record_id=record_id
    )

    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return record_to_response(db, record)


@router.put("/{record_id}")
def update_existing_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db)
):
    try:
        record = update_record(
            db=db,
            record_id=record_id,
            data=payload.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return record_to_response(db, record)
