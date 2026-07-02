from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document_config import (
    DocumentType,
    DocumentExtractionField,
    ExcelColumnMapping
)
from app.services.admin_service import get_process


# =========================
# Document Types
# =========================

def create_document_type(db: Session, data: dict) -> DocumentType:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    existing = (
        db.query(DocumentType)
        .filter(
            DocumentType.process_id == data["process_id"],
            DocumentType.code == data["code"]
        )
        .first()
    )

    if existing:
        raise ValueError(f"Ya existe un tipo de documento con el código: {data['code']}")

    document_type = DocumentType(
        process_id=data["process_id"],
        code=data["code"],
        name=data["name"],
        description=data.get("description"),
        direction=data.get("direction", "input"),
        allowed_extensions=data.get("allowed_extensions"),
        is_required=data.get("is_required", False),
        is_ai_enabled=data.get("is_ai_enabled", True),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(document_type)
    db.commit()
    db.refresh(document_type)

    return document_type


def list_document_types(db: Session, process_id: int | None = None) -> list[DocumentType]:
    query = db.query(DocumentType)

    if process_id:
        query = query.filter(DocumentType.process_id == process_id)

    return query.order_by(DocumentType.name.asc()).all()


def get_document_type(db: Session, document_type_id: int) -> DocumentType | None:
    return (
        db.query(DocumentType)
        .filter(DocumentType.id == document_type_id)
        .first()
    )


def update_document_type(db: Session, document_type_id: int, data: dict) -> DocumentType | None:
    document_type = get_document_type(db, document_type_id)

    if not document_type:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(document_type, key, value)

    document_type.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(document_type)

    return document_type


# =========================
# Extraction Fields
# =========================

def create_extraction_field(db: Session, data: dict) -> DocumentExtractionField:
    document_type = get_document_type(db, data["document_type_id"])

    if not document_type:
        raise ValueError("Tipo de documento no encontrado.")

    item = DocumentExtractionField(
        document_type_id=data["document_type_id"],
        source_name=data["source_name"],
        target_entity=data["target_entity"],
        target_field=data["target_field"],
        extraction_type=data.get("extraction_type", "ai"),
        is_required=data.get("is_required", False),
        instructions=data.get("instructions")
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def list_extraction_fields(
    db: Session,
    document_type_id: int
) -> list[DocumentExtractionField]:
    return (
        db.query(DocumentExtractionField)
        .filter(DocumentExtractionField.document_type_id == document_type_id)
        .order_by(DocumentExtractionField.id.asc())
        .all()
    )


def get_extraction_field(
    db: Session,
    extraction_field_id: int
) -> DocumentExtractionField | None:
    return (
        db.query(DocumentExtractionField)
        .filter(DocumentExtractionField.id == extraction_field_id)
        .first()
    )


def update_extraction_field(
    db: Session,
    extraction_field_id: int,
    data: dict
) -> DocumentExtractionField | None:
    item = get_extraction_field(db, extraction_field_id)

    if not item:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# =========================
# Excel Column Mappings
# =========================

def create_excel_mapping(db: Session, data: dict) -> ExcelColumnMapping:
    document_type = get_document_type(db, data["document_type_id"])

    if not document_type:
        raise ValueError("Tipo de documento no encontrado.")

    item = ExcelColumnMapping(
        document_type_id=data["document_type_id"],
        sheet_name=data.get("sheet_name"),
        header_row=data.get("header_row", 1),
        column_name=data["column_name"],
        target_entity=data["target_entity"],
        target_field=data["target_field"],
        is_required=data.get("is_required", False)
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def list_excel_mappings(
    db: Session,
    document_type_id: int
) -> list[ExcelColumnMapping]:
    return (
        db.query(ExcelColumnMapping)
        .filter(ExcelColumnMapping.document_type_id == document_type_id)
        .order_by(ExcelColumnMapping.id.asc())
        .all()
    )


def get_excel_mapping(
    db: Session,
    mapping_id: int
) -> ExcelColumnMapping | None:
    return (
        db.query(ExcelColumnMapping)
        .filter(ExcelColumnMapping.id == mapping_id)
        .first()
    )


def update_excel_mapping(
    db: Session,
    mapping_id: int,
    data: dict
) -> ExcelColumnMapping | None:
    item = get_excel_mapping(db, mapping_id)

    if not item:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item
