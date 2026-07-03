from dataclasses import asdict
from pathlib import Path

from sqlalchemy.orm import Session

from app.engines.document_intelligence.document_intelligence_factory import (
    get_document_intelligence_engine
)
from app.engines.documents.pdf_reader import extract_text_from_pdf
from app.engines.documents.text_document_reader import (
    extract_text_from_docx,
    extract_text_from_eml,
    extract_text_from_msg
)
from app.models.document import Document


def extract_text_for_understanding(document: Document) -> str:
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

    raise ValueError(f"Tipo no soportado para comprensión documental: {extension}")


def understand_document(db: Session, document_id: int) -> dict:
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

    text = extract_text_for_understanding(document)

    engine = get_document_intelligence_engine()
    understanding = engine.understand_document(text)

    document.ai_summary = understanding.summary or document.ai_summary
    document.processing_status = "understood"

    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "understanding": asdict(understanding)
    }
