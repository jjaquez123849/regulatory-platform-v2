from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_processing_service import process_document


router = APIRouter(
    prefix="/document-processing",
    tags=["Document Processing"]
)


@router.post("/{document_id}/process")
def process_uploaded_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    try:
        return process_document(
            db=db,
            document_id=document_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
