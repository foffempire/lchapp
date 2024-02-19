from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List


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


