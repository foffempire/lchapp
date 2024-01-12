from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas_admin, utils, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List
from fastapi.responses import JSONResponse
import shutil
import os


router = APIRouter(
    tags=['category']
)
# ***************UPLOAD CATEGORY IMAGE*******************
@router.post("/admin_category/upload/")
def upload_category_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/category/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"
    
    allowed_extension = ['png', 'jpg', "jpeg", 'PNG', 'JPG', 'JPEG']

    if file_extension not in allowed_extension:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"file format not allowed, only jpg, png, and jpeg are allowed")
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
    


# ***************ADD CATEGORY*******************
@router.post("/admin_category", status_code=status.HTTP_201_CREATED)
def add_category(cat: schemas_admin.Category, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):

    insert = models.Category( **cat.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************DELETE CATEGORY*******************
@router.delete("/admin_category/{id}", status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    stmt = db.query(models.Category).filter(models.Category.id == id)
    if stmt.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'not found')
    
    stmt.delete(synchronize_session=False)
    db.commit()
    return {"data": "record deleted"}


# ***************GET ALL CATEGORY*******************
@router.get("/admin_category", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.CategoryResponse])
def get_all_category(db: Session = Depends(get_db)):
    category = db.query(models.Category).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category


# ***************GET PARENT CATEGORY*******************
@router.get("/admin_category/main", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.CategoryResponse])
def get_parent_category(db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.parent_id == 0).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category


# ***************GET PARENT CATEGORY*******************
@router.get("/admin_category/{parent_id}", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.CategoryResponse])
def get_sub_category(parent_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.parent_id == parent_id).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category