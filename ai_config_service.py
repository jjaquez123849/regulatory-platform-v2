from datetime import datetime
from sqlalchemy.orm import Session

from app.models.ai_config import AIConfiguration
from app.services.admin_service import get_process


def create_ai_configuration(db: Session, data: dict) -> AIConfiguration:
    process = get_process(db, data["process_id"])

    if not process:
        raise ValueError("Proceso no encontrado.")

    item = AIConfiguration(
        process_id=data["process_id"],
        document_type_id=data.get("document_type_id"),
        name=data["name"],
        purpose=data["purpose"],
        instructions=data.get("instructions"),
        expected_output=data.get("expected_output"),
        is_active=data.get("is_active", True),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def list_ai_configurations(
    db: Session,
    process_id: int | None = None,
    document_type_id: int | None = None,
    purpose: str | None = None
) -> list[AIConfiguration]:
    query = db.query(AIConfiguration)

    if process_id:
        query = query.filter(AIConfiguration.process_id == process_id)

    if document_type_id:
        query = query.filter(AIConfiguration.document_type_id == document_type_id)

    if purpose:
        query = query.filter(AIConfiguration.purpose == purpose)

    return query.order_by(AIConfiguration.created_at.desc()).all()
