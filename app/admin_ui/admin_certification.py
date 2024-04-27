from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import  get_db
from sqlalchemy.orm import Session 
from typing import List



router = APIRouter(
    tags=['Admin certification']
)



# ***************GET CERTIFICATE*******************
@router.get('/certifications/{business_id}', status_code=status.HTTP_200_OK, response_model=List[schemas_admin.CertResponse])
def get_certificates(business_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Certifications).filter(models.Certifications.business_id == business_id).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query


@router.get('/certification/{cert_id}', status_code=status.HTTP_200_OK, response_model=schemas_admin.CertResponse)
def view_single_certificate(cert_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Certifications).filter(models.Certifications.id == cert_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query


# ***************DELETE CERTIFICATE*******************
@router.delete('/certification/{cert_id}')
def delete_certificate(cert_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Certifications).filter(models.Certifications.id == cert_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate not found")


    query.delete(synchronize_session=False)
    db.commit()
    return{"data":"deleted"}



# ***************APPROVE CERTIFICATE*******************
@router.post('/cert_approval/{business_id}', status_code=status.HTTP_200_OK)
def approve_cert(business_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Business).filter(models.Business.business_id == business_id).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with {business_id} found")

    query.has_valid_cert = 1
    return {"data":"approved"}



