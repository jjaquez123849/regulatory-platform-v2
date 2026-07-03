from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_understanding_service import understand_document


router = APIRouter(
    prefix="/document-understanding",
    tags=["Document Understanding"]
)


@router.post("/{document_id}/understand")
def understand_uploaded_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    try:
        return understand_document(
            db=db,
            document_id=document_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
