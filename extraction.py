from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import DocumentExtractionResult
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
            "confidence_score": item.confidence_score,
            "status": item.status,
            "reviewed_by": item.reviewed_by,
            "reviewed_at": item.reviewed_at,
            "created_at": item.created_at
        }
        for item in results
    ]


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
