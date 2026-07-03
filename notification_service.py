from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification


def list_notifications(
    db: Session,
    recipient_user: str | None = None,
    recipient_area: str | None = None,
    status: str | None = None
) -> list[Notification]:
    query = db.query(Notification).filter(Notification.is_deleted == False)

    if recipient_user:
        query = query.filter(Notification.recipient_user == recipient_user)

    if recipient_area:
        query = query.filter(Notification.recipient_area == recipient_area)

    if status:
        query = query.filter(Notification.status == status)

    return query.order_by(Notification.created_at.desc()).all()


def mark_notification_read(
    db: Session,
    notification_id: int
) -> Notification | None:
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.is_deleted == False
        )
        .first()
    )

    if not notification:
        return None

    notification.status = "read"
    notification.read_at = datetime.utcnow()

    db.commit()
    db.refresh(notification)

    return notification
