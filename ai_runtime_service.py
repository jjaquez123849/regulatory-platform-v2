from sqlalchemy.orm import Session

from app.models.ai_config import AIConfiguration


def get_active_ai_instructions(
    db: Session,
    process_id: int,
    document_type_id: int | None = None,
    purpose: str = "extraction"
) -> str | None:
    query = (
        db.query(AIConfiguration)
        .filter(
            AIConfiguration.process_id == process_id,
            AIConfiguration.purpose == purpose,
            AIConfiguration.is_active == True
        )
    )

    if document_type_id:
        specific = (
            query
            .filter(AIConfiguration.document_type_id == document_type_id)
            .order_by(AIConfiguration.created_at.desc())
            .first()
        )

        if specific:
            return specific.instructions

    general = (
        query
        .filter(AIConfiguration.document_type_id == None)
        .order_by(AIConfiguration.created_at.desc())
        .first()
    )

    return general.instructions if general else None
