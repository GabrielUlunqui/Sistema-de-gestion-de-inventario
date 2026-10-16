from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/", response_model=schemas.Stats)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)
