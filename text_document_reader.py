from pathlib import Path
from email import policy
from email.parser import BytesParser

import docx
from sqlalchemy.orm import Session

from app.engines.ai.ai_engine_factory import get_ai_engine
from app.models.document import Document, DocumentExtractionResult
from app.models.document_config import DocumentExtractionField


def extract_text_from_eml(file_path: Path) -> str:
    with open(file_path, "rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    parts = []

    subject = message.get("subject")
    sender = message.get("from")
    date = message.get("date")

    if subject:
        parts.append(f"Subject: {subject}")
    if sender:
        parts.append(f"From: {sender}")
    if date:
        parts.append(f"Date: {date}")

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()

            if content_type == "text/plain":
                parts.append(part.get_content())
    else:
        parts.append(message.get_content())

    return "\n".join(parts).strip()


def extract_text_from_msg(file_path: Path) -> str:
    try:
        import extract_msg
    except ImportError:
        raise ValueError("La librería extract-msg no está instalada.")

    msg = extract_msg.Message(str(file_path))

    parts = []

    if msg.subject:
        parts.append(f"Subject: {msg.subject}")
    if msg.sender:
        parts.append(f"From: {msg.sender}")
    if msg.date:
        parts.append(f"Date: {msg.date}")
    if msg.body:
        parts.append(msg.body)

    return "\n".join(parts).strip()


def extract_text_from_docx(file_path: Path) -> str:
    document = docx.Document(str(file_path))
    return "\n".join([p.text for p in document.paragraphs]).strip()


def read_text_document_with_config(
    db: Session,
    document: Document
) -> dict:
    if not document.document_type_id:
        raise ValueError("El documento no tiene tipo de documento configurado.")

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise ValueError("El archivo físico no existe.")

    extension = (document.file_extension or "").lower()

    if extension == "eml":
        text = extract_text_from_eml(file_path)
    elif extension == "msg":
        text = extract_text_from_msg(file_path)
    elif extension == "docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Tipo de documento de texto no soportado: {extension}")

    extraction_fields = (
        db.query(DocumentExtractionField)
        .filter(DocumentExtractionField.document_type_id == document.document_type_id)
        .all()
    )

    if not extraction_fields:
        raise ValueError("No hay campos de extracción configurados para este tipo de documento.")

    results = []
    errors = []

    if not text:
        errors.append("No se pudo extraer texto del documento.")

    ai_engine = get_ai_engine(db)
    ai_results = ai_engine.extract_fields(
        text=text,
        extraction_fields=extraction_fields
    )

    for ai_result in ai_results:
        extraction = DocumentExtractionResult(
            document_id=document.id,
            record_id=document.record_id,
            target_entity=ai_result.target_entity,
            target_field=ai_result.target_field,
            extracted_value=str(ai_result.value),
            normalized_value=str(ai_result.value).strip(),
            confidence_score=str(ai_result.confidence_score),
            status="proposed"
        )

        db.add(extraction)

        results.append(
            {
                "target_entity": ai_result.target_entity,
                "target_field": ai_result.target_field,
                "value": ai_result.value,
                "confidence_score": ai_result.confidence_score,
                "explanation": ai_result.explanation
            }
        )

    document.ai_summary = ai_engine.summarize(text) if text else None
    document.ai_confidence = "0.55" if results else "0.0"
    document.processing_status = "text_extracted" if not errors else "text_extracted_with_errors"

    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "text_preview": text[:1000],
        "results_count": len(results),
        "results": results,
        "errors": errors
    }
