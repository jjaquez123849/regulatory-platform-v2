from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models.security import User
from app.services.rkf_service import (
    get_rkf_document,
    get_rkf_rir,
    list_rkf_documents,
    save_rkf_rir,
    validate_rkf_rir,
)


router = APIRouter(
    prefix="/rkf",
    tags=["Regulatory Knowledge Factory"],
)


@router.get("/documents")
def read_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_rkf_documents()


@router.get("/documents/{document_id}")
def read_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_rkf_document(document_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/documents/{document_id}/rir")
def read_document_rir(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_rkf_rir(document_id)


@router.post("/documents/{document_id}/rir")
def save_document_rir(
    document_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return save_rkf_rir(document_id=document_id, rir=payload)


@router.post("/documents/{document_id}/validate")
def validate_document_rir(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return validate_rkf_rir(document_id)
