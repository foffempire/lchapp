from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session 
from typing import List
import shutil
import os
from ..utils import baseURL



router = APIRouter(
    tags=['catalog']
)


def verify_owner(cid, uid, db):
    
    biz = db.query(models.Business).filter(models.Business.owner_id == uid).first()
    cert = db.query(models.Catalog).filter(models.Catalog.id == cid).first()
    if biz.id == cert.business_id:
        return True


# ***************UPLOAD CATALOG IMAGE*******************
@router.post("/catalog/upload/")
def upload_catalog_image(files: List[UploadFile] = File(...) ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/catalog/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    uploaded_images = []
    
    for file in files:
        # Generate a unique filename for the uploaded image
        file_extension = file.filename.split(".")[-1]
        newfilename = f"{utils.generate_unique_id(15)}.{file_extension}"

        # For demonstration purposes, we'll just store the filename and content type.
        file_name = newfilename
        uploaded_images.append(file_name)

        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+newfilename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


    #convert list to strings
    # initialize an empty string
    # string_output = ""
 
    # # traverse in the string
    # for ele in uploaded_images:
    #     string_output += f"{ele},"
    

    # #remove the last comma
    # string_output = string_output[:-1]

    # # return string
    # return string_output

    return uploaded_images
 
 
# ***************ADD CATALOG*******************
@router.post("/catalog", status_code=status.HTTP_200_OK, response_model=schemas.CatalogResponse)
def add_catalog(catalog: schemas.Catalog, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Business not found")
    
    biz_id = query.first().id
    insert = models.Catalog(business_id = biz_id, name = catalog.name, price = catalog.price, description = catalog.description)
    db.add(insert)
    db.commit()
    db.refresh(insert)

    for files in catalog.images:
        add = models.CatalogImg(catalog_id = insert.id, image = files)
        db.add(add)
        db.commit()

    return insert



# ***************UPDATE CATALOG*******************
@router.put("/catalog/{id}", status_code=status.HTTP_200_OK)
def update_catalog(id: int, catalog: schemas.Catalog, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Catalog).filter(models.Catalog.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catalog not found")
    
    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to update this catalog")
    
    query.update(catalog.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()

   

# ***************DELETE CATALOG*******************
@router.delete('/catalog/{id}')
def delete_catalog(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Catalog).filter(models.Catalog.id == id)
    queryImg = db.query(models.CatalogImg).filter(models.CatalogImg.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Catalog not found")


    if not verify_owner(id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete this catalog")


    query.delete(synchronize_session=False)
    queryImg.delete(synchronize_session=False)
    db.commit()

    return{"data":"deleted"}


# ***************GET CATALOG*******************
@router.get('/catalog/{catalog_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CatalogResponse])
def get_catalog(catalog_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Catalog).filter(models.Catalog.id == catalog_id).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No catalogs found")   
    return query


@router.get('/explore_catalogs/', status_code=status.HTTP_200_OK, response_model=List[schemas.CatalogExplore])
def explore_catalogs(db: Session = Depends(get_db)):
    query = db.query(models.CatalogImg).order_by(func.random()).limit(50)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No catalogs found")   
    return query

