from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_schema import (
    DocumentTypeCreate,
    DocumentTypeUpdate,
    DocumentTypeResponse,
    DocumentExtractionFieldCreate,
    DocumentExtractionFieldUpdate,
    DocumentExtractionFieldResponse,
    ExcelColumnMappingCreate,
    ExcelColumnMappingUpdate,
    ExcelColumnMappingResponse
)
from app.services.document_config_service import (
    create_document_type,
    list_document_types,
    get_document_type,
    update_document_type,
    create_extraction_field,
    list_extraction_fields,
    get_extraction_field,
    update_extraction_field,
    create_excel_mapping,
    list_excel_mappings,
    get_excel_mapping,
    update_excel_mapping
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin - Documents"]
)


# =========================
# Document Types
# =========================

@router.post("/document-types", response_model=DocumentTypeResponse)
def create_new_document_type(
    payload: DocumentTypeCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_document_type(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/document-types", response_model=list[DocumentTypeResponse])
def read_document_types(
    process_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    return list_document_types(
        db=db,
        process_id=process_id
    )


@router.get("/document-types/{document_type_id}", response_model=DocumentTypeResponse)
def read_document_type(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    document_type = get_document_type(db, document_type_id)

    if not document_type:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

    return document_type


@router.put("/document-types/{document_type_id}", response_model=DocumentTypeResponse)
def update_existing_document_type(
    document_type_id: int,
    payload: DocumentTypeUpdate,
    db: Session = Depends(get_db)
):
    document_type = update_document_type(
        db=db,
        document_type_id=document_type_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not document_type:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

    return document_type


# =========================
# Extraction Fields
# =========================

@router.post("/extraction-fields", response_model=DocumentExtractionFieldResponse)
def create_new_extraction_field(
    payload: DocumentExtractionFieldCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_extraction_field(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get(
    "/document-types/{document_type_id}/extraction-fields",
    response_model=list[DocumentExtractionFieldResponse]
)
def read_extraction_fields(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    return list_extraction_fields(
        db=db,
        document_type_id=document_type_id
    )


@router.get("/extraction-fields/{extraction_field_id}", response_model=DocumentExtractionFieldResponse)
def read_extraction_field(
    extraction_field_id: int,
    db: Session = Depends(get_db)
):
    item = get_extraction_field(db, extraction_field_id)

    if not item:
        raise HTTPException(status_code=404, detail="Campo de extracción no encontrado")

    return item


@router.put("/extraction-fields/{extraction_field_id}", response_model=DocumentExtractionFieldResponse)
def update_existing_extraction_field(
    extraction_field_id: int,
    payload: DocumentExtractionFieldUpdate,
    db: Session = Depends(get_db)
):
    item = update_extraction_field(
        db=db,
        extraction_field_id=extraction_field_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not item:
        raise HTTPException(status_code=404, detail="Campo de extracción no encontrado")

    return item


# =========================
# Excel Column Mappings
# =========================

@router.post("/excel-mappings", response_model=ExcelColumnMappingResponse)
def create_new_excel_mapping(
    payload: ExcelColumnMappingCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_excel_mapping(db, payload.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get(
    "/document-types/{document_type_id}/excel-mappings",
    response_model=list[ExcelColumnMappingResponse]
)
def read_excel_mappings(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    return list_excel_mappings(
        db=db,
        document_type_id=document_type_id
    )


@router.get("/excel-mappings/{mapping_id}", response_model=ExcelColumnMappingResponse)
def read_excel_mapping(
    mapping_id: int,
    db: Session = Depends(get_db)
):
    item = get_excel_mapping(db, mapping_id)

    if not item:
        raise HTTPException(status_code=404, detail="Mapeo Excel no encontrado")

    return item


@router.put("/excel-mappings/{mapping_id}", response_model=ExcelColumnMappingResponse)
def update_existing_excel_mapping(
    mapping_id: int,
    payload: ExcelColumnMappingUpdate,
    db: Session = Depends(get_db)
):
    item = update_excel_mapping(
        db=db,
        mapping_id=mapping_id,
        data=payload.model_dump(exclude_unset=True)
    )

    if not item:
        raise HTTPException(status_code=404, detail="Mapeo Excel no encontrado")

    return item
