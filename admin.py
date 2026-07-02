from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_schema import (
    ProcessCreate,
    ProcessUpdate,
    ProcessResponse,
    ProcessFieldCreate,
    ProcessFieldUpdate,
    ProcessFieldResponse,
    FieldOptionCreate,
    FieldOptionUpdate,
    FieldOptionResponse
)
from app.services.admin_service import (
    create_process,
    list_processes,
    get_process,
    update_process,
    create_process_field,
    list_process_fields,
    get_process_field,
    update_process_field,
    create_field_option,
    list_field_options,
    get_field_option,
    update_field_option,
    get_full_process_config
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/processes", response_model=ProcessResponse)
def create_new_process(payload: ProcessCreate, db: Session = Depends(get_db)):
    try:
        return create_process(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/processes", response_model=list[ProcessResponse])
def read_processes(db: Session = Depends(get_db)):
    return list_processes(db)


@router.get("/processes/{process_id}", response_model=ProcessResponse)
def read_process(process_id: int, db: Session = Depends(get_db)):
    process = get_process(db, process_id)

    if not process:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")

    return process


@router.put("/processes/{process_id}", response_model=ProcessResponse)
def update_existing_process(
    process_id: int,
    payload: ProcessUpdate,
    db: Session = Depends(get_db)
):
    process = update_process(
        db=db,
        process_id=process_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not process:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")

    return process


@router.get("/processes/{process_id}/config")
def read_full_process_config(process_id: int, db: Session = Depends(get_db)):
    try:
        config = get_full_process_config(db, process_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    return {
        "process": ProcessResponse.model_validate(config["process"]),
        "fields": [
            ProcessFieldResponse.model_validate(field)
            for field in config["fields"]
        ]
    }


@router.post("/fields", response_model=ProcessFieldResponse)
def create_new_field(payload: ProcessFieldCreate, db: Session = Depends(get_db)):
    try:
        return create_process_field(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/processes/{process_id}/fields", response_model=list[ProcessFieldResponse])
def read_process_fields(process_id: int, db: Session = Depends(get_db)):
    return list_process_fields(db, process_id)


@router.get("/fields/{field_id}", response_model=ProcessFieldResponse)
def read_field(field_id: int, db: Session = Depends(get_db)):
    field = get_process_field(db, field_id)

    if not field:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    return field


@router.put("/fields/{field_id}", response_model=ProcessFieldResponse)
def update_existing_field(
    field_id: int,
    payload: ProcessFieldUpdate,
    db: Session = Depends(get_db)
):
    field = update_process_field(
        db=db,
        field_id=field_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not field:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    return field


@router.post("/field-options", response_model=FieldOptionResponse)
def create_new_field_option(
    payload: FieldOptionCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_field_option(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/fields/{field_id}/options", response_model=list[FieldOptionResponse])
def read_field_options(field_id: int, db: Session = Depends(get_db)):
    return list_field_options(db, field_id)


@router.get("/field-options/{option_id}", response_model=FieldOptionResponse)
def read_field_option(option_id: int, db: Session = Depends(get_db)):
    option = get_field_option(db, option_id)

    if not option:
        raise HTTPException(status_code=404, detail="Opción no encontrada")

    return option


@router.put("/field-options/{option_id}", response_model=FieldOptionResponse)
def update_existing_field_option(
    option_id: int,
    payload: FieldOptionUpdate,
    db: Session = Depends(get_db)
):
    option = update_field_option(
        db=db,
        option_id=option_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not option:
        raise HTTPException(status_code=404, detail="Opción no encontrada")

    return option
