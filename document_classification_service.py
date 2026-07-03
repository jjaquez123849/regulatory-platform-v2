from pathlib import Path

from sqlalchemy.orm import Session

from app.engines.ai.ai_engine_factory import get_ai_engine
from app.engines.documents.pdf_reader import extract_text_from_pdf
from app.engines.documents.text_document_reader import (
    extract_text_from_docx,
    extract_text_from_eml,
    extract_text_from_msg
)
from app.models.document import Document
from app.models.document_config import DocumentType
from app.services.record_service import get_record


def extract_text_for_classification(document: Document) -> str:
    file_path = Path(document.file_path)

    if not file_path.exists():
        raise ValueError("El archivo físico no existe.")

    extension = (document.file_extension or "").lower()

    if extension == "pdf":
        return extract_text_from_pdf(file_path)

    if extension == "eml":
        return extract_text_from_eml(file_path)

    if extension == "msg":
        return extract_text_from_msg(file_path)

    if extension == "docx":
        return extract_text_from_docx(file_path)

    return ""


def classify_document(db: Session, document_id: int) -> dict:
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

    if not document:
        raise ValueError("Documento no encontrado.")

    if not document.record_id:
        raise ValueError("El documento debe estar asociado a un registro para clasificarlo.")

    record = get_record(db, document.record_id)

    if not record:
        raise ValueError("Registro no encontrado.")

    document_types = (
        db.query(DocumentType)
        .filter(DocumentType.process_id == record.process_id)
        .all()
    )

    if not document_types:
        raise ValueError("No hay tipos de documentos configurados para este proceso.")

    text = extract_text_for_classification(document)

    ai_engine = get_ai_engine(db)

    result = ai_engine.classify_document(
        text=text,
        document_types=document_types
    )

    if result.get("document_type_id"):
        document.document_type_id = result["document_type_id"]
        document.processing_status = "classified"
        db.commit()
        db.refresh(document)

    return {
        "document_id": document.id,
        "document_type_id": document.document_type_id,
        "confidence_score": result.get("confidence_score"),
        "reason": result.get("reason"),
        "status": document.processing_status
    }
