from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Request
from .. import models, schemas_admin, utils, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List
from fastapi.responses import JSONResponse
import shutil
import os
from fastapi.templating import Jinja2Templates
from ..utils import baseURL
import requests, json


router = APIRouter(
    tags=['Admin category']
)

# Jinja2 templating
templates = Jinja2Templates(directory="admin_files")


cateImgUrl = "uploads/category/"
# ***************UPLOAD CATEGORY IMAGE*******************
@router.post("/admin_category/upload/")
def upload_category_image(file: UploadFile):

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
        
        return {"filename" : cateImgUrl+filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
    


# ***************ADD CATEGORY*******************
@router.post("/admin_category/", status_code=status.HTTP_201_CREATED)
# def add_category(cat: schemas_admin.Category, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def add_category(cat: schemas_admin.Category, db: Session = Depends(get_db) ):
    stmt = db.query(models.Category).filter(models.Category.name == cat.name).first()
    
    if stmt:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Category already exist')
  
    insert = models.Category( **cat.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************DELETE CATEGORY*******************
@router.post("/admin_category/{id}", status_code=status.HTTP_200_OK)
# def delete_category(id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def delete_category(id: int, db: Session = Depends(get_db) ):
    stmt = db.query(models.Category).filter(models.Category.id == id).first()
    
    if not stmt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category not found')
    
    stmt.is_active = False
    db.commit()
    return {"data": "record deleted"}


# ***************GET ALL CATEGORY*******************
@router.get("/admin_category/", status_code=status.HTTP_200_OK)
# def get_all_category(request: Request, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def get_all_category(request: Request, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.is_active == True).order_by(models.Category.name).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    # return category
    
    def getParent(pid):    
        req = requests.get(f'{baseURL}admin_category/{pid}')
        return req.json()
    
    return templates.TemplateResponse(request=request, name="category.html", context={"category": category, "baseURL": baseURL, "pid": getParent})


# ***************GET ALL PARENT CATEGORY*******************
@router.get("/admin_category/main/", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.CategoryResponse])
# def get_all_parent_category(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def get_all_parent_category(db: Session = Depends(get_db) ):
    category = db.query(models.Category).filter(models.Category.parent_id == 0).all()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
    return category


# ***************GET PARENT CATEGORY*******************
@router.get("/admin_category/{parent_id}", status_code=status.HTTP_200_OK)
# def get_sub_category(parent_id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
def get_parent_category(parent_id: int, db: Session = Depends(get_db)):

    if(parent_id == 0):        
        return "None"
    
    else:
        category = db.query(models.Category).filter(models.Category.id == parent_id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found!")
        return category.name
    

