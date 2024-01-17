from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2_admin

router = APIRouter(
    tags=["Admin"]
)

@router.post("/admin/login", response_model=schemas.Token)
def login(userlogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    userlogin.username = userlogin.username.lower()
    user = db.query(models.Admin).filter(models.Admin.username == userlogin.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")
    
    verfy_pass = utils.verify_password(userlogin.password, user.password)
    if not verfy_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")
    

    #create a token
    access_token = oauth2_admin.create_access_token(data = {"username": user.username})

    # return token
    return {"access_token": access_token, "token_type":"bearer"}
