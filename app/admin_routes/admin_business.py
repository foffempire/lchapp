from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List


router = APIRouter(
    tags=['Admin business']
)

   


# ***************GET SINGLE BUSINESSES*******************
@router.get("/admin/business/{id}", status_code=status.HTTP_200_OK, response_model=schemas_admin.Business)
def get_single_business( id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    results =  db.query(models.Business).filter(models.Business.id == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found.")
    
    return results


# ***************GET ALL BUSINESSES*******************
@router.get("/admin/businesses/", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.Business])
# def get_all_businesses(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def get_all_businesses(db: Session = Depends(get_db)):

    # query all businesses
    results =  db.query(models.Business).order_by(models.Business.name).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" NO business found.")
    
    return results


# ***************GET SUBSCRIBED BUSINESSES*******************
@router.get("/admin/subscribed_businesses/", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.Business])
# def get_all_subscribed_businesses(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def get_all_subscribed_businesses(db: Session = Depends(get_db)):

    
    # query only subscribed businesses
    results =  db.query(models.Business).join(models.Subscription, models.Business.id == models.Subscription.business_id).filter(models.Subscription.is_active == True).all()
    

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" No Active subscriber.")
    
    return results



# ***************COUNT BUSINESSES*******************
@router.get("/admin/count_business/", status_code=status.HTTP_200_OK)
def count_businesses(db: Session = Depends(get_db)):
# def count_businesses(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    results =  db.query(func.count(models.Business.id).label("total_biz")).scalar()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="0")
    
    return results



# ***************COUNT SUBSCRIBED BUSINESSES*******************
@router.get("/admin/count_subscribed_businesses/", status_code=status.HTTP_200_OK)
def count_businesses(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    

    results = db.query(models.Business).join(models.Subscription, models.Business.id == models.Subscription.business_id).filter(models.Subscription.is_active == True).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="0")
    
    return len(results)


