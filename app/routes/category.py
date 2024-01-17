from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List
from fastapi.responses import JSONResponse
import shutil
import os
import uuid


router = APIRouter(
    tags=['category']
)

# ***************GET ALL CATEGORY*******************
@router.get("/category", status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryResponse])
def get_all_category(db: Session = Depends(get_db)):
    category = db.query(models.Category).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category


# ***************GET PARENT CATEGORY*******************
@router.get("/category/main", status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryResponse])
def get_parent_category(db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.parent_id == 0).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category


# ***************GET PARENT CATEGORY*******************
@router.get("/category/{parent_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryResponse])
def get_sub_category(parent_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.parent_id == parent_id).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category