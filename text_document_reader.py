from pathlib import Path
from email import policy
from email.parser import BytesParser

import docx
from sqlalchemy.orm import Session

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


def simple_rule_extract(text: str, source_name: str) -> str | None:
    lower_source = source_name.lower()

    for line in text.splitlines():
        line_clean = line.strip()
        line_lower = line_clean.lower()

        if lower_source in line_lower:
            parts = line_clean.split(":")
            if len(parts) > 1:
                return parts[-1].strip()
            return line_clean

    return None


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

    for field in extraction_fields:
        value = simple_rule_extract(
            text=text,
            source_name=field.source_name
        )

        if not value:
            if field.is_required:
                errors.append(f"No se encontró campo requerido: {field.source_name}")
            continue

        extraction = DocumentExtractionResult(
            document_id=document.id,
            record_id=document.record_id,
            target_entity=field.target_entity,
            target_field=field.target_field,
            extracted_value=value,
            normalized_value=value.strip(),
            confidence_score="0.50",
            status="proposed"
        )

        db.add(extraction)

        results.append(
            {
                "source_name": field.source_name,
                "target_entity": field.target_entity,
                "target_field": field.target_field,
                "value": value,
                "confidence_score": "0.50"
            }
        )

    document.ai_summary = text[:2000] if text else None
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
