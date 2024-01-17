from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List


router = APIRouter(
    tags=['Admin Subscription']
)


# ***************GET SUBSCRIPTION HISROTY*******************
@router.get("/admin/subhistory/{id}", status_code=status.HTTP_200_OK)
def get_sub_history( id: int, db: Session = Depends(get_db)):
    results =  db.query(models.SubHistory).filter(models.SubHistory.business_id == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found.")
    
    return results

