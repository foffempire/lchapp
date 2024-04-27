from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
from ..utils import get_password_hash, verify_password

router = APIRouter(
    tags=["Admin Details"]
)



# ***************REGISTER USER******************
@router.post("/admin/register", status_code=status.HTTP_201_CREATED, response_model=schemas_admin.AdminOut)
async def register(user: schemas_admin.RegisterAdminUser, db: Session = Depends(get_db)):
    user.username = user.username.lower()
    #username exist
    username_exist = db.query(models.Admin).filter(models.Admin.username == user.username).first()
    if username_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exist")
    
    user.password = get_password_hash(user.password)
    new_uza =  models.Admin(**user.model_dump())
    db.add(new_uza)
    db.commit()
    db.refresh(new_uza)
    return new_uza



# ***************PERSONAL DETAILS*******************
@router.post("/admin/me/", status_code=status.HTTP_201_CREATED, response_model=schemas_admin.AdminOut)
def update_details(user: schemas_admin.Personal, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    query = db.query(models.Admin).filter(models.Admin.username == admin_user.username)
    
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(user.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    


# ***************UPDATE PASSWORD*******************
@router.post("/admin/me/password/", status_code=status.HTTP_202_ACCEPTED)
def update_password(user: schemas_admin.Password, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):

    user.password = get_password_hash(user.password)

    query = db.query(models.Admin).filter(models.Admin.id == admin_user.id)
    
    #user exist
    user_exist = query.first()
    if user_exist:
        verfy_pass = verify_password(user.old_password, user_exist.password)
        if not verfy_pass:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")
        
        query.update({"password": user.password}, synchronize_session=False)
        db.commit()
        return {"data": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User doesn't exist")
    



# ***************GET USER DETAILS*******************
@router.get("/admin/me/", status_code=status.HTTP_200_OK, response_model=schemas_admin.AdminOut)
def get_details(db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    results =  db.query(models.Admin).filter(admin_user.username == models.Admin.username).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No personal details found.")
    
    return results


