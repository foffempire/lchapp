from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from ..database import get_db
router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(userlogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    userlogin.username = userlogin.username.lower()
    user = db.query(models.User).filter(models.User.email == userlogin.username, models.User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")
    
    verfy_pass = utils.verify_password(userlogin.password, user.password)
    if not verfy_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details")
    

    if not user.email_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Verify your email to continue")

    #create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type":"bearer"}


# @router.post("/logout")
# def user_logout(Authorization: str = Header(None)):
#     oauth2.oauth2_scheme.revoke_token(Authorization)
#     return {"message": "Token revoked"}


# ***************DELETE ACCOUNT*******************
@router.post("/deactaccount/", status_code=status.HTTP_200_OK)
def account(input: schemas.RegisterUser,  db: Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.email == input.email, models.User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
    

    verfy_pass = utils.verify_password(input.password, user.password)
    if not verfy_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user details")
    
    biz = db.query(models.Business).filter(models.Business.owner_id == user.id).first()
    
    
    if biz:
        biz.is_active = False

    user.is_active = False

    db.commit()
    return {"data": "deleted"}
