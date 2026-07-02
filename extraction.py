from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import DocumentExtractionResult
from app.schemas.extraction_schema import ExtractionResultUpdate
from app.services.extraction_apply_service import apply_extraction_results


router = APIRouter(
    prefix="/extraction",
    tags=["Extraction"]
)


@router.get("/documents/{document_id}/results")
def read_extraction_results(
    document_id: int,
    db: Session = Depends(get_db)
):
    results = (
        db.query(DocumentExtractionResult)
        .filter(DocumentExtractionResult.document_id == document_id)
        .order_by(DocumentExtractionResult.id.asc())
        .all()
    )

    return [
        {
            "id": item.id,
            "document_id": item.document_id,
            "record_id": item.record_id,
            "target_entity": item.target_entity,
            "target_field": item.target_field,
            "extracted_value": item.extracted_value,
            "normalized_value": item.normalized_value,
            "source_sheet": item.source_sheet,
            "source_row": item.source_row,
            "source_column": item.source_column,
            "source_group_key": item.source_group_key,
            "confidence_score": item.confidence_score,
            "status": item.status,
            "reviewed_by": item.reviewed_by,
            "reviewed_at": item.reviewed_at,
            "created_at": item.created_at
        }
        for item in results
    ]


@router.put("/results/{result_id}")
def update_extraction_result(
    result_id: int,
    payload: ExtractionResultUpdate,
    db: Session = Depends(get_db)
):
    result = (
        db.query(DocumentExtractionResult)
        .filter(DocumentExtractionResult.id == result_id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Resultado de extracción no encontrado")

    data = payload.model_dump(exclude_unset=True)

    if "normalized_value" in data:
        result.normalized_value = data["normalized_value"]

    if "status" in data:
        allowed_status = ["proposed", "approved", "rejected", "corrected", "applied"]

        if data["status"] not in allowed_status:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Permitidos: {', '.join(allowed_status)}"
            )

        result.status = data["status"]

    if "reviewed_by" in data:
        result.reviewed_by = data["reviewed_by"]
        result.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(result)

    return {
        "id": result.id,
        "document_id": result.document_id,
        "record_id": result.record_id,
        "target_entity": result.target_entity,
        "target_field": result.target_field,
        "extracted_value": result.extracted_value,
        "normalized_value": result.normalized_value,
        "status": result.status,
        "reviewed_by": result.reviewed_by,
        "reviewed_at": result.reviewed_at
    }


@router.post("/documents/{document_id}/apply")
def apply_document_extraction_results(
    document_id: int,
    performed_by: str | None = Query(None),
    db: Session = Depends(get_db)
):
    try:
        return apply_extraction_results(
            db=db,
            document_id=document_id,
            performed_by=performed_by
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
