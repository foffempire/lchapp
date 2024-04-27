from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import  get_db
from sqlalchemy.orm import Session 
from typing import List



router = APIRouter(
    tags=['Admin ID card']
)



# ***************GET ID CARD*******************
@router.get('/admin/identities/', status_code=status.HTTP_200_OK, response_model=List[schemas_admin.IdentityResponse])
def get_id(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Identity).join(models.Business, models.Identity.business_id == models.Business.id).filter(models.Business.has_valid_id == 0, models.Identity.disapproved == 0)
    print(query)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No identity found")   
    return query.all()



@router.get('/admin/identity/{card_id}', status_code=status.HTTP_200_OK, response_model=schemas_admin.IdentityResponse)
def get_id(card_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Identity).filter(models.Identity.id == card_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No identity found")   
    return query


# ***************DELETE IDENTITY*******************
@router.delete('/admin/identity/{identity_id}')
def delete_id(identity_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Identity).filter(models.Identity.id == identity_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Identity not found")


    query.delete(synchronize_session=False)
    db.commit()
    return{"data":"deleted"}



# ***************APPROVE ID CARD*******************
@router.post('/id_approval/{business_id}', status_code=status.HTTP_200_OK)
def approve_id(business_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Business).filter(models.Business.business_id == business_id).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with {business_id} found")

    query.has_valid_id = 1
    # send mail
    return {"data":"approved"}




