from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.notification_service import (
    list_notifications,
    mark_notification_read
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/")
def read_notifications(
    recipient_user: str | None = Query(None),
    recipient_area: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):
    notifications = list_notifications(
        db=db,
        recipient_user=recipient_user,
        recipient_area=recipient_area,
        status=status
    )

    return [
        {
            "id": item.id,
            "record_id": item.record_id,
            "title": item.title,
            "message": item.message,
            "recipient_user": item.recipient_user,
            "recipient_area": item.recipient_area,
            "priority": item.priority,
            "status": item.status,
            "created_at": item.created_at,
            "read_at": item.read_at
        }
        for item in notifications
    ]


@router.put("/{notification_id}/read")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = mark_notification_read(
        db=db,
        notification_id=notification_id
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    return {
        "id": notification.id,
        "status": notification.status,
        "read_at": notification.read_at
    }
