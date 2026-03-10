from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, noload
import auth
import models
import schemas
from database import get_db, get_object_or_404

# router = APIRouter(dependencies=[Depends(auth.get_current_user)])
router = APIRouter()

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)) -> List[models.Category]:
    # return db.query(models.Category).all()
    return db.query(models.Category).options(noload(models.Category.documents)).all()


@router.get("/{id}", response_model=schemas.Category)
def read_category(category: models.Category = Depends(get_object_or_404(models.Category))) -> models.Category:
    return category


@router.get("/{id}/documents", response_model=List[schemas.Document])
def read_documents_by_category(
    category: models.Category = Depends(get_object_or_404(models.Category)),
    db: Session = Depends(get_db),
) -> List[models.Document]:
    documents: List[models.Document] = (
        db.query(models.Document)
        .filter(models.Document.category_id == category.id)
        .all()
    )
    return documents


@router.put("/{id}", response_model=schemas.Category)
def update_category(
    category_update: schemas.CategoryUpdate,
    category: models.Category = Depends(get_object_or_404(models.Category)),
    db: Session = Depends(get_db),
) -> models.Category:
    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category = Depends(get_object_or_404(models.Category)),
    db: Session = Depends(get_db),
) -> None:
    db.delete(category)
    db.commit()
    return