from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter(prefix="/attributes", tags=["Attributes"])

@router.get("/")
def list_attributes(db: Session = Depends(get_db)):
    return {"status": "ok", "message": "Attributes router working"}
