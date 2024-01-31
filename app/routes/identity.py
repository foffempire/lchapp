from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import  get_db
from sqlalchemy.orm import Session 
from typing import List
from ..utils import baseURL
from fastapi.responses import JSONResponse
import shutil
import os



router = APIRouter(
    tags=['Identity Card']
)

# idImgUrl = f"{baseURL}uploads/identity/"
idImgUrl = "uploads/identity/"


# ***************UPLOAD ID CARD IMAGE*******************
@router.post("/identity/upload/")
def upload_id(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/identity/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"
    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : idImgUrl+filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
    

# ***************ADD IDENTITY*******************
@router.post("/identity", status_code=status.HTTP_200_OK, response_model=schemas.IdentityResponse)
def add_identity_card(idc: schemas.Identity, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Register a business first")
    
    biz_id = query.first().id
    insert = models.Identity(business_id = biz_id, **idc.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)

    # notify admin
    # notify()
    return insert


