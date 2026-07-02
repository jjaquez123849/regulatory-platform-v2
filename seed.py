from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.seed_service import seed_regulatory_requests


router = APIRouter(
    prefix="/seed",
    tags=["Seed"]
)


@router.post("/regulatory-requests")
def create_regulatory_seed(db: Session = Depends(get_db)):
    return seed_regulatory_requests(db)
