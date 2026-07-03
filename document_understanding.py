import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_understanding_service import (
    understand_document,
    list_document_understandings
)


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


@router.get("/{document_id}/history")
def read_document_understanding_history(
    document_id: int,
    db: Session = Depends(get_db)
):
    items = list_document_understandings(
        db=db,
        document_id=document_id
    )

    return [
        {
            "id": item.id,
            "document_id": item.document_id,
            "record_id": item.record_id,
            "document_type": item.document_type,
            "issuer": item.issuer,
            "regulator": item.regulator,
            "subject": item.subject,
            "summary": item.summary,
            "request_number": item.request_number,
            "request_date": item.request_date,
            "due_date": item.due_date,
            "entities": json.loads(item.entities_json or "[]"),
            "requests": json.loads(item.requests_json or "[]"),
            "metadata": json.loads(item.metadata_json or "{}"),
            "created_at": item.created_at,
        }
        for item in items
    ]
