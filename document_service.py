import shutil
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_config import DocumentType
from app.models.audit import AuditLog
from app.services.record_service import get_record


BASE_DIR = Path(__file__).resolve().parents[2]
UPLOADS_DIR = BASE_DIR / "data" / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def get_document_type(db: Session, document_type_id: int) -> DocumentType | None:
    return (
        db.query(DocumentType)
        .filter(DocumentType.id == document_type_id)
        .first()
    )


def validate_file_extension(document_type: DocumentType, filename: str) -> None:
    extension = filename.split(".")[-1].lower() if "." in filename else ""

    allowed_raw = document_type.allowed_extensions or ""
    allowed = [
        item.strip().lower()
        for item in allowed_raw.split(",")
        if item.strip()
    ]

    if allowed and extension not in allowed:
        raise ValueError(
            f"Extensión no permitida. Permitidas: {', '.join(allowed)}"
        )


def upload_document(
    db: Session,
    file: UploadFile,
    record_id: int | None,
    document_type_id: int | None,
    uploaded_by: str | None = None
) -> Document:
    record = None
    document_type = None

    if record_id is not None:
        record = get_record(db, record_id)

        if not record:
            raise ValueError("Registro no encontrado.")

    if document_type_id is not None:
        document_type = get_document_type(db, document_type_id)

        if not document_type:
            raise ValueError("Tipo de documento no encontrado.")

        validate_file_extension(document_type, file.filename)

    extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""

    target_dir = UPLOADS_DIR

    if record_id is not None:
        target_dir = UPLOADS_DIR / str(record_id)

    target_dir.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid4().hex}.{extension}" if extension else uuid4().hex
    stored_path = target_dir / stored_filename

    with stored_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = Document(
        record_id=record_id,
        document_type_id=document_type_id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(stored_path),
        file_extension=extension,
        mime_type=file.content_type,
        direction=document_type.direction if document_type else "input",
        processing_status="uploaded",
        uploaded_by=uploaded_by,
        uploaded_at=datetime.utcnow()
    )

    db.add(document)
    db.flush()

    db.add(
        AuditLog(
            record_id=record_id,
            entity_type="document",
            entity_id=document.id,
            action="UPLOAD_DOCUMENT",
            details=f"Documento cargado: {file.filename}",
            performed_by=uploaded_by
        )
    )

    db.commit()
    db.refresh(document)

    return document


def list_documents(db: Session, record_id: int | None = None) -> list[Document]:
    query = db.query(Document).filter(Document.is_deleted == False)

    if record_id is not None:
        query = query.filter(Document.record_id == record_id)

    return query.order_by(Document.uploaded_at.desc()).all()


def get_document(db: Session, document_id: int) -> Document | None:
    return (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )
