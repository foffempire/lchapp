from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy import func, or_
from sqlalchemy.orm import Session 
from typing import List
from fastapi.responses import JSONResponse
import shutil
import os
from PIL import Image


router = APIRouter(
    tags=['business']
)


bannerImgUrl = "uploads/banner/"

# ***************ADD BUSINESS NAME/ABOUT*******************
@router.post("/business", status_code=status.HTTP_201_CREATED, response_model=schemas.Business)
def add_business(biz: schemas.BusinessAbout, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    random = utils.generate_unique_id(15)

    itag = f"{biz.name}, {biz.about}, {biz.category}"
    # iloc = f"{biz.town}, {biz.lga}"
    iloc = f"{biz.lga}"
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(biz.model_dump(), location = iloc, synchronize_session=False)
        query.first().tag = itag
        db.commit()
        return query.first()
    else:
        insert = models.Business(owner_id = current_user.id, location = iloc,  bid = random, tag = itag, **biz.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert
    

# ***************UPDATE BUSINESS NAME/ABOUT*******************
@router.put("/business", status_code=status.HTTP_201_CREATED, response_model=schemas.Business)
def update_business(biz: schemas.BusinessAbout, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    random = utils.generate_unique_id(15)

    itag = f"{biz.name}, {biz.about}, {biz.category}"
    # iloc = f"{biz.town}, {biz.lga}"
    iloc = f"{biz.lga}"
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        query.first().tag = itag
        query.first().location = iloc
        db.commit()
        return query.first()

    


# ***************UPLOAD BANNER IMAGE*******************
@router.post("/business/upload/")
def upload_banner_image(file: UploadFile ):


    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/banner/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"
    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

            # resize image
            base_width= 500
            img = Image.open(f"{UPLOAD_DIRECTORY}/{filename}")
            wpercent = (base_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
            img.save(f"{UPLOAD_DIRECTORY}/{filename}")
        
        return {"filename" : bannerImgUrl+filename}

    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
 


# ***************ADD/UPDATE BANNER*******************
@router.post("/business/image", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def banner_image(biz: schemas.BusinessImage, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
 


# ***************ADD/UPDATE LOCATION*******************
@router.post("/business/location", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_map_location(loc: schemas.BusinessLocation, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)
    if query.first():
        query.update(loc.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
 

 



# ***************ADD/UPDATE WORKING DAYS AND TIME*******************
@router.post("/business/schedule", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_schedule(biz: schemas.BusinessHour, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    


# ***************ADD/UPDATE SOCIAL HANDLES*******************
@router.post("/business/social", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_social_media(biz: schemas.BusinessSocial, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    

# ***************GET LOGGED IN USER BUSINESS AND DETAILS*******************
@router.get("/business", status_code=status.HTTP_200_OK, response_model=schemas.Business)
def get_my_business(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    results =  db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found, create a business.")
    
    return results


# ***************GET SINGLE BUSINESSES*******************
@router.get("/business/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Business)
def get_single_business( id: int, db: Session = Depends(get_db)):
    results =  db.query(models.Business).filter(models.Business.id == id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found.")
    
    return results


# ***************GET ALL BUSINESSES*******************
@router.get("/businesses", status_code=status.HTTP_200_OK, response_model=List[schemas.Business])
def get_all_businesses(db: Session = Depends(get_db), limit: int = 50, skip: int = 0):

    # query all businesses
    results =  db.query(models.Business).limit(limit).offset(skip).all()

    """
    # query only subscribed businesses (needed when there area subscribers)
    results =  db.query(models.Business).join(models.Subscription, models.Business.id == models.Subscription.business_id).filter(models.Subscription.is_active == True).limit(limit).offset(skip).all()
    """

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" No business found.")
    
    return results



# ***************SEARCH/QUERY BUSINESSES*******************
@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[schemas.Business])
def query_businesses(db: Session = Depends(get_db), search: str = '', limit: int  = 50, skip:int = 0, location: str = ''):


    results =  db.query(models.Business).filter(func.lower(models.Business.tag).like('%' +func.lower(search) + '%'), func.lower(models.Business.location).like('%' +func.lower(location) + '%')).limit(limit=limit).offset(skip).all()
  

    

    """
    #search only subscribed businesss
    results =  db.query(models.Business).join(models.Subscription).filter(func.lower(models.Business.tag).like('%' +func.lower(search) + '%'), func.lower(models.Business.location).like('%' +func.lower(location) + '%'), models.Subscription.is_active == True).limit(limit=limit).offset(skip).all()
    """
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found.")
    
    insert = models.SearchHistory(search = search.lower())
    db.add(insert)
    db.commit()

    return results


# ***************GET SEARCH SUGGESTIONS*******************
@router.get("/search_suggest/{search}", status_code=status.HTTP_200_OK)
def search_suggest(search: str, db: Session = Depends(get_db)):

    search=search.lower()
    # recent = db.query(models.SearchHistory).distinct(models.SearchHistory.search).filter((models.SearchHistory.search).like('%' +search + '%')).limit(3).all()


    recent = db.query(models.Category).filter(func.lower(models.Category.name).like('%' +search + '%'))
                      
    if not recent.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business found!")
    
    return recent.all()


# ***************SAVE/FAVORITE A BUSINESS*******************
@router.post("/savebusiness/{business_id}", status_code=status.HTTP_200_OK)
def save_businesses(business_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    # check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found.")
    
    
    # check if already saved
    stmt = db.query(models.Favorite).filter(models.Favorite.business_id == business_id, models.Favorite.user_id == current_user.id)
    if stmt.first():
        stmt.delete(synchronize_session=False)
        db.commit()
        return{"result":"deleted"}
    
    else:    
        insert = models.Favorite(user_id = current_user.id, business_id = business_id)
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return{"result":"saved"}
    


@router.get("/savebusiness/", status_code=status.HTTP_200_OK, response_model=List[schemas.Favorite])
def my_saved_businesses(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    stmt = db.query(models.Favorite).filter(models.Favorite.user_id == current_user.id)
    return stmt.all()



# ***************GET VIP BUSINESSES*******************
@router.get("/vip", status_code=status.HTTP_200_OK, response_model=List[schemas.Business])
def get_vip_businesses(db: Session = Depends(get_db), limit: int = 50, skip: int = 0):

    """
    results =  db.query(models.Business).join(models.Subscription, models.Business.id == models.Subscription.business_id).filter(models.Subscription.is_active == True).limit(limit).offset(skip).all()

    """
    # query only VIP businesses (needed when there are VIP subscribers)
    results =  db.query(models.Business).filter(models.Business.is_vip == 1).limit(limit).offset(skip).all()
    

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" No business found.")
    
    return results




"""
# ***************ADD/UPDATE EXPERIENCE*******************
@router.post("/business/experience", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_experience(biz: schemas.BusinessExperience, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    

# ***************ADD/UPDATE ADDRESS*******************
@router.post("/business/address", status_code = status.HTTP_201_CREATED, response_model=schemas.Business)
def update_address(biz: schemas.BusinessAddress, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Business).filter(models.Business.owner_id == current_user.id)

    biz_exist = query.first()
    if biz_exist:
        query.update(biz.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found, create a business first")
    
"""