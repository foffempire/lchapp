from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func



router = APIRouter(
    tags=['rating']
)

  

# ***************ADD RATING******************
@router.post("/rating/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Rating)
def add_rating(business_id: int, rate: schemas.Rating, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Rating).filter(models.Rating.business_id == business_id, models.Rating.user_id == current_user.id)

    biz = db.query(models.Business).filter(models.Business.id == business_id)

    if not biz.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id}!")
    
    if biz.first().owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot rate your own business!")
     
    if query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You already rated this business!")
    
    if rate.rating < 1 or rate.rating > 5:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You can only rate from 1 - 5!")
    
    insert = models.Rating(business_id = business_id, user_id = current_user.id, **rate.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert



# ***************GET RATING******************
@router.get('/rating/{business_id}', status_code=status.HTTP_200_OK)
def get_rating(business_id: int, db: Session = Depends(get_db)):

    biz = db.query(models.Rating).filter(models.Rating.business_id == business_id)

    if not biz.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no rating for business with id of {business_id}")

    query = db.query(func.round(func.avg(models.Rating.rating),1).label('rounded')).filter(models.Rating.business_id == business_id).all() 
    
    return query[0][0]