from datetime import datetime

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.record import Record


def create_comment(db: Session, data: dict) -> Comment:
    record = (
        db.query(Record)
        .filter(
            Record.id == data["record_id"],
            Record.is_deleted == False,
        )
        .first()
    )

    if not record:
        raise ValueError("Registro no encontrado.")

    comment = Comment(
        record_id=data["record_id"],
        comment_text=data["comment_text"],
        comment_type=data.get("comment_type", "general"),
        created_by=data.get("created_by"),
        created_at=datetime.utcnow(),
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def list_comments(db: Session, record_id: int) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(
            Comment.record_id == record_id,
            Comment.is_deleted == False,
        )
        .order_by(Comment.created_at.desc())
        .all()
    )
