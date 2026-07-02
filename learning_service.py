from datetime import datetime

from sqlalchemy.orm import Session

from app.models.document import Document, DocumentExtractionResult
from app.models.learning import ExtractionLearningExample


def create_learning_example_from_result(
    db: Session,
    result_id: int,
    created_by: str | None = None
) -> ExtractionLearningExample:
    result = (
        db.query(DocumentExtractionResult)
        .filter(DocumentExtractionResult.id == result_id)
        .first()
    )

    if not result:
        raise ValueError("Resultado de extracción no encontrado.")

    document = (
        db.query(Document)
        .filter(Document.id == result.document_id)
        .first()
    )

    if not document:
        raise ValueError("Documento no encontrado.")

    if not result.normalized_value:
        raise ValueError("No hay valor corregido/aprobado para guardar como aprendizaje.")

    example = ExtractionLearningExample(
        process_id=None,
        document_type_id=document.document_type_id,
        target_entity=result.target_entity,
        target_field=result.target_field,
        original_value=result.extracted_value,
        corrected_value=result.normalized_value,
        source_context=f"{result.source_sheet or ''} | row={result.source_row} | col={result.source_column}",
        source_file_extension=document.file_extension,
        created_by=created_by,
        created_at=datetime.utcnow()
    )

    db.add(example)
    db.commit()
    db.refresh(example)

    return example


def list_learning_examples(
    db: Session,
    document_type_id: int | None = None,
    target_entity: str | None = None,
    target_field: str | None = None
) -> list[ExtractionLearningExample]:
    query = db.query(ExtractionLearningExample)

    if document_type_id:
        query = query.filter(ExtractionLearningExample.document_type_id == document_type_id)

    if target_entity:
        query = query.filter(ExtractionLearningExample.target_entity == target_entity)

    if target_field:
        query = query.filter(ExtractionLearningExample.target_field == target_field)

    return query.order_by(ExtractionLearningExample.created_at.desc()).all()
