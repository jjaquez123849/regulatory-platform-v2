from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.automation_schema import AutomationRunRequest
from app.services.automation_engine_service import run_automation_event


router = APIRouter(
    prefix="/automation",
    tags=["Automation Engine"]
)


@router.post("/run")
def run_automation(
    payload: AutomationRunRequest,
    db: Session = Depends(get_db)
):
    try:
        return run_automation_event(
            db=db,
            process_id=payload.process_id,
            trigger_event=payload.trigger_event,
            context=payload.context
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
