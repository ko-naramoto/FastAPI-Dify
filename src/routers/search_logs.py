from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

# router = APIRouter(dependencies=[Depends(auth.get_current_user)])
router = APIRouter()

@router.post("/", response_model=schemas.SearchLog, status_code=status.HTTP_201_CREATED)
def create_search_log(log: schemas.SearchLogCreate, db: Session = Depends(get_db)):
    if log.category_id:
        category = db.get(models.Category, log.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
    db_log = models.SearchLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/", response_model=List[schemas.SearchLog])
def read_search_logs(db: Session = Depends(get_db)):
    logs = (
        db.query(models.SearchLog)
        .order_by(models.SearchLog.created_at.desc())
        .all()
    )
    return logs