from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.quality_service import (
    run_quality_review,
    list_quality_reviews,
    list_quality_issues
)


router = APIRouter(
    prefix="/quality",
    tags=["Quality Review"]
)


@router.post("/records/{record_id}/run")
def run_record_quality_review(
    record_id: int,
    document_id: int | None = Query(None),
    reviewed_by: str | None = Query(None),
    db: Session = Depends(get_db)
):
    try:
        review = run_quality_review(
            db=db,
            record_id=record_id,
            document_id=document_id,
            reviewed_by=reviewed_by
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "id": review.id,
        "record_id": review.record_id,
        "document_id": review.document_id,
        "status": review.status,
        "score": review.score,
        "summary": review.summary,
        "has_missing_items": review.has_missing_items,
        "missing_items": review.missing_items,
        "reviewed_by": review.reviewed_by,
        "reviewed_at": review.reviewed_at
    }


@router.get("/records/{record_id}/reviews")
def read_quality_reviews(
    record_id: int,
    db: Session = Depends(get_db)
):
    reviews = list_quality_reviews(
        db=db,
        record_id=record_id
    )

    return [
        {
            "id": item.id,
            "record_id": item.record_id,
            "document_id": item.document_id,
            "status": item.status,
            "score": item.score,
            "summary": item.summary,
            "has_missing_items": item.has_missing_items,
            "missing_items": item.missing_items,
            "reviewed_by": item.reviewed_by,
            "reviewed_at": item.reviewed_at
        }
        for item in reviews
    ]


@router.get("/records/{record_id}/issues")
def read_quality_issues(
    record_id: int,
    only_open: bool = Query(True),
    db: Session = Depends(get_db)
):
    issues = list_quality_issues(
        db=db,
        record_id=record_id,
        only_open=only_open
    )

    return [
        {
            "id": item.id,
            "review_id": item.review_id,
            "record_id": item.record_id,
            "issue_type": item.issue_type,
            "severity": item.severity,
            "description": item.description,
            "related_person_id": item.related_person_id,
            "related_request_item_id": item.related_request_item_id,
            "is_resolved": item.is_resolved,
            "resolved_by": item.resolved_by,
            "resolved_at": item.resolved_at,
            "created_at": item.created_at
        }
        for item in issues
    ]
