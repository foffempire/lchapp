from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session 
from typing import List
from ..utils import baseURL
from fastapi.responses import JSONResponse
import shutil
import os
import uuid



router = APIRouter(
    tags=['certification']
)

# certImgUrl = f"{baseURL}uploads/certificate/"
certImgUrl = "uploads/certificate/"

def verify_owner(cid, uid, db):
    
    biz = db.query(models.Business).filter(models.Business.owner_id == uid).first()
    cert = db.query(models.Certifications).filter(models.Certifications.id == cid).first()
    if biz.id == cert.business_id:
        return True


# ***************UPLOAD CERTIFICATE IMAGE*******************
@router.post("/certification/upload/")
def upload_certificate_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/certificate/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"
    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : certImgUrl+filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
    

# ***************ADD CERTIFICATE*******************
@router.post("/certification", status_code=status.HTTP_200_OK, response_model=schemas.CertResponse)
def add_certificate(cert: schemas.Cert, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Register a business first")
    
    biz_id = query.first().id
    insert = models.Certifications(business_id = biz_id, **cert.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************UPDATE CERTIFICATE*******************
@router.put("/certification/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CertResponse)
def update_certificate(id: int, cert: schemas.Cert, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Certifications).filter(models.Certifications.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate not found")
    

    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to update this certificate")
    

    query.update(cert.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()



# ***************DELETE CERTIFICATE*******************
@router.delete('/certification/{id}')
def delete_certificate(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Certifications).filter(models.Certifications.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Certificate not found")

    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete this certificate")
    

    query.delete(synchronize_session=False)
    db.commit()
    return{"data":"deleted"}



# ***************GET CERTIFICATE*******************
@router.get('/certifications/{business_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CertResponse])
def get_certificates(business_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Certifications).filter(models.Certifications.business_id == business_id).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query


@router.get('/certification/{cert_id}', status_code=status.HTTP_200_OK, response_model=schemas.CertResponse)
def view_single_certificate(cert_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Certifications).filter(models.Certifications.id == cert_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query