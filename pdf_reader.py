from pathlib import Path

import pdfplumber
from sqlalchemy.orm import Session

from app.engines.ai.ai_engine_factory import get_ai_engine
from app.models.document import Document, DocumentExtractionResult
from app.models.document_config import DocumentExtractionField
from app.services.ai_runtime_service import get_active_ai_instructions
from app.services.record_service import get_record


def extract_text_from_pdf(file_path: Path) -> str:
    text_parts = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    return "\n".join(text_parts).strip()


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

    process_id = None

    if document.record_id:
        record = get_record(db, document.record_id)
        if record:
            process_id = record.process_id

    instructions = None

    if process_id:
        instructions = get_active_ai_instructions(
            db=db,
            process_id=process_id,
            document_type_id=document.document_type_id,
            purpose="extraction"
        )

    ai_engine = get_ai_engine(db)
    ai_results = ai_engine.extract_fields(
        text=text,
        extraction_fields=extraction_fields,
        instructions=instructions
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
    document.ai_confidence = "0.60" if results else "0.0"
    document.processing_status = "pdf_extracted" if not errors else "pdf_extracted_with_errors"

    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "text_preview": text[:1000],
        "instructions_used": bool(instructions),
        "results_count": len(results),
        "results": results,
        "errors": errors
    }
