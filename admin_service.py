from datetime import datetime
from sqlalchemy.orm import Session

from app.models.configuration import Process, ProcessField, FieldOption


# =========================
# Processes
# =========================

def create_process(db: Session, data: dict) -> Process:
    existing = (
        db.query(Process)
        .filter(Process.code == data["code"])
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe un proceso con el código: {data['code']}")

    if data.get("is_default"):
        db.query(Process).update({"is_default": False})

    process = Process(
        code=data["code"],
        name=data["name"],
        description=data.get("description"),
        is_default=data.get("is_default", False),
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(process)
    db.commit()
    db.refresh(process)

    return process


def list_processes(db: Session) -> list[Process]:
    return (
        db.query(Process)
        .order_by(Process.name.asc())
        .all()
    )


def get_process(db: Session, process_id: int) -> Process | None:
    return (
        db.query(Process)
        .filter(Process.id == process_id)
        .first()
    )


def update_process(db: Session, process_id: int, data: dict) -> Process | None:
    process = get_process(db, process_id)

    if not process:
        return None

    if data.get("is_default") is True:
        db.query(Process).update({"is_default": False})

    for field, value in data.items():
        if value is not None:
            setattr(process, field, value)

    process.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(process)

    return process


# =========================
# Fields
# =========================

def create_process_field(db: Session, data: dict) -> ProcessField:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    existing = (
        db.query(ProcessField)
        .filter(
            ProcessField.process_id == data["process_id"],
            ProcessField.name == data["name"]
        )
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe un campo con el nombre: {data['name']}")

    field = ProcessField(
        process_id=data["process_id"],
        name=data["name"],
        label=data["label"],
        field_type=data["field_type"],
        is_required=data.get("is_required", False),
        is_visible=data.get("is_visible", True),
        is_editable=data.get("is_editable", True),
        is_exportable=data.get("is_exportable", True),
        display_order=data.get("display_order", 0),
        help_text=data.get("help_text"),
        default_value=data.get("default_value"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(field)
    db.commit()
    db.refresh(field)

    return field


def list_process_fields(db: Session, process_id: int) -> list[ProcessField]:
    return (
        db.query(ProcessField)
        .filter(ProcessField.process_id == process_id)
        .order_by(ProcessField.display_order.asc(), ProcessField.id.asc())
        .all()
    )


def get_process_field(db: Session, field_id: int) -> ProcessField | None:
    return (
        db.query(ProcessField)
        .filter(ProcessField.id == field_id)
        .first()
    )


def update_process_field(db: Session, field_id: int, data: dict) -> ProcessField | None:
    field = get_process_field(db, field_id)

    if not field:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(field, key, value)

    field.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(field)

    return field


# =========================
# Field Options
# =========================

def create_field_option(db: Session, data: dict) -> FieldOption:
    field = get_process_field(db, data["field_id"])

    if not field:
        raise ValueError("Campo no encontrado.")

    option = FieldOption(
        field_id=data["field_id"],
        value=data["value"],
        label=data["label"],
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True)
    )

    db.add(option)
    db.commit()
    db.refresh(option)

    return option


def list_field_options(db: Session, field_id: int) -> list[FieldOption]:
    return (
        db.query(FieldOption)
        .filter(FieldOption.field_id == field_id)
        .order_by(FieldOption.display_order.asc(), FieldOption.id.asc())
        .all()
    )


def get_field_option(db: Session, option_id: int) -> FieldOption | None:
    return (
        db.query(FieldOption)
        .filter(FieldOption.id == option_id)
        .first()
    )


def update_field_option(db: Session, option_id: int, data: dict) -> FieldOption | None:
    option = get_field_option(db, option_id)

    if not option:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(option, key, value)

    db.commit()
    db.refresh(option)

    return option


def get_full_process_config(db: Session, process_id: int) -> dict:
    process = get_process(db, process_id)

    if not process:
        raise ValueError("Proceso no encontrado.")

    fields = list_process_fields(db, process_id)

    return {
        "process": process,
        "fields": fields
    }
