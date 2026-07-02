from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.document_service import (
    upload_document,
    list_documents,
    get_document
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_new_document(
    file: UploadFile = File(...),
    record_id: int | None = Form(None),
    document_type_id: int | None = Form(None),
    uploaded_by: str | None = Form(None),
    db: Session = Depends(get_db)
):
    try:
        document = upload_document(
            db=db,
            file=file,
            record_id=record_id,
            document_type_id=document_type_id,
            uploaded_by=uploaded_by
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "id": document.id,
        "record_id": document.record_id,
        "document_type_id": document.document_type_id,
        "original_filename": document.original_filename,
        "stored_filename": document.stored_filename,
        "file_extension": document.file_extension,
        "mime_type": document.mime_type,
        "direction": document.direction,
        "processing_status": document.processing_status,
        "uploaded_by": document.uploaded_by,
        "uploaded_at": document.uploaded_at
    }


@router.get("/")
def read_documents(
    record_id: int | None = None,
    db: Session = Depends(get_db)
):
    documents = list_documents(
        db=db,
        record_id=record_id
    )

    return [
        {
            "id": item.id,
            "record_id": item.record_id,
            "document_type_id": item.document_type_id,
            "original_filename": item.original_filename,
            "stored_filename": item.stored_filename,
            "file_extension": item.file_extension,
            "mime_type": item.mime_type,
            "direction": item.direction,
            "processing_status": item.processing_status,
            "ai_summary": item.ai_summary,
            "ai_confidence": item.ai_confidence,
            "uploaded_by": item.uploaded_by,
            "uploaded_at": item.uploaded_at
        }
        for item in documents
    ]


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = get_document(db, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

    return FileResponse(
        path=file_path,
        filename=document.original_filename,
        media_type=document.mime_type or "application/octet-stream"
    )
