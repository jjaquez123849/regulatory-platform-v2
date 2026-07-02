from pathlib import Path

import pdfplumber
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentExtractionResult
from app.models.document_config import DocumentExtractionField


def extract_text_from_pdf(file_path: Path) -> str:
    text_parts = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def simple_rule_extract(text: str, source_name: str) -> str | None:
    """
    Extracción básica inicial.
    Luego esto será reemplazado/reforzado por IA local o asistida.
    """
    lower_text = text.lower()
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


def read_pdf_with_config(
    db: Session,
    document: Document
) -> dict:
    if not document.document_type_id:
        raise ValueError("El documento no tiene tipo de documento configurado.")

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise ValueError("El archivo físico no existe.")

    extraction_fields = (
        db.query(DocumentExtractionField)
        .filter(DocumentExtractionField.document_type_id == document.document_type_id)
        .all()
    )

    if not extraction_fields:
        raise ValueError("No hay campos de extracción configurados para este tipo de documento.")

    text = extract_text_from_pdf(file_path)

    results = []
    errors = []

    if not text:
        errors.append("No se pudo extraer texto del PDF. Puede ser escaneado o imagen.")

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
    document.processing_status = "pdf_extracted" if not errors else "pdf_extracted_with_errors"

    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "text_preview": text[:1000],
        "results_count": len(results),
        "results": results,
        "errors": errors
    }
