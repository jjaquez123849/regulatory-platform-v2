from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_classification_service import classify_document


router = APIRouter(
    prefix="/document-classification",
    tags=["Document Classification"]
)


@router.post("/{document_id}/classify")
def classify_uploaded_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    try:
        return classify_document(
            db=db,
            document_id=document_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
