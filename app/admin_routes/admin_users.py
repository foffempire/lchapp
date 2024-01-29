from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List

router = APIRouter(
    tags=["Admin User"]
)


#get all users
@router.get("/admin/users/", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.UserOut])
def get_users(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    uza =  db.query(models.User).all()
    return uza


#get all users
@router.get("/admin/user/{id}", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.UserOut])
def get_users(id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    uza =  db.query(models.User).filter(models.User.id == id)

    if(uza.first()):
        return uza



@router.get("/admin/countusers/", status_code=status.HTTP_200_OK)
def count_users(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    results =  db.query(func.count(models.User.id).label("total_uza")).scalar()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" No Users found.")
    

    return results

