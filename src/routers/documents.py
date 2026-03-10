from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import auth
import models
import schemas
from database import get_db, get_object_or_404

router = APIRouter(dependencies=[Depends(auth.get_current_user)])

@router.post("/", response_model=schemas.Document, status_code=status.HTTP_201_CREATED)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    category = db.get(models.Category, document.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get("/", response_model=List[schemas.Document])
def read_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).all()
    return documents


@router.get("/{id}", response_model=schemas.Document)
def read_document(document: models.Document = Depends(get_object_or_404(models.Document))):
    return document


@router.put("/{id}", response_model=schemas.Document)
def update_document(
    document_update: schemas.DocumentUpdate,
    document: models.Document = Depends(get_object_or_404(models.Document)),
    db: Session = Depends(get_db),
):
    update_data = document_update.model_dump(exclude_unset=True)
    if "category_id" in update_data and update_data["category_id"] is not None:
        category = db.get(models.Category, update_data["category_id"])
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

    for key, value in update_data.items():
        setattr(document, key, value)
    db.commit()
    db.refresh(document)
    return document


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document: models.Document = Depends(get_object_or_404(models.Document)),
    db: Session = Depends(get_db),
):
    db.delete(document)
    db.commit()
    return