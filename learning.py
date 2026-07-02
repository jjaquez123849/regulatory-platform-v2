from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.learning_service import (
    create_learning_example_from_result,
    list_learning_examples
)


router = APIRouter(
    prefix="/learning",
    tags=["Learning"]
)


@router.post("/from-result/{result_id}")
def create_learning_from_result(
    result_id: int,
    created_by: str | None = Query(None),
    db: Session = Depends(get_db)
):
    try:
        example = create_learning_example_from_result(
            db=db,
            result_id=result_id,
            created_by=created_by
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "id": example.id,
        "document_type_id": example.document_type_id,
        "target_entity": example.target_entity,
        "target_field": example.target_field,
        "original_value": example.original_value,
        "corrected_value": example.corrected_value,
        "created_by": example.created_by,
        "created_at": example.created_at
    }


@router.get("/")
def read_learning_examples(
    document_type_id: int | None = Query(None),
    target_entity: str | None = Query(None),
    target_field: str | None = Query(None),
    db: Session = Depends(get_db)
):
    examples = list_learning_examples(
        db=db,
        document_type_id=document_type_id,
        target_entity=target_entity,
        target_field=target_field
    )

    return [
        {
            "id": item.id,
            "process_id": item.process_id,
            "document_type_id": item.document_type_id,
            "target_entity": item.target_entity,
            "target_field": item.target_field,
            "original_value": item.original_value,
            "corrected_value": item.corrected_value,
            "source_context": item.source_context,
            "source_file_extension": item.source_file_extension,
            "created_by": item.created_by,
            "created_at": item.created_at
        }
        for item in examples
    ]
