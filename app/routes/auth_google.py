from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
import requests
import random
from ..config import settings


router = APIRouter(
    tags=["Google Authentication"]
)
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_client_id}&redirect_uri={settings.google_redirect_uri}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth/google")
async def auth_google(code: str, db: Session = Depends(database.get_db)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})

    userData = user_info.json()

    #check if user exist
    query = db.query(models.User).filter(models.User.email == userData["email"])

    if query.first():
        #create a token
        access_token = oauth2.create_access_token(data = {"user_id": query.first().id})

        # return token
        return {"access_token": access_token, "token_type":"bearer"}

    else:
        verification_code = random.randint(100000, 999999)
        new_uza =  models.User(verification_code = verification_code, email = userData["email"],password="password", firstname = userData["given_name"], lastname = userData["family_name"], email_verified = 1)
        db.add(new_uza)
        db.commit()
        db.refresh(new_uza)

        #create a token
        access_token = oauth2.create_access_token(data = {"user_id": new_uza.id})

        # return token
        return {"id": new_uza.id, "email": new_uza.email, "access_token": access_token, "token_type":"bearer"}



    # result = []
    # result.append(user_info.json())
    # result.append(access_token)
    # return result

"""
@router.get("/auth/google")
async def auth_google(email: str, firstname: str = '', lastname: str = '', db: Session = Depends(database.get_db)):
   
    #check if user exist
    query = db.query(models.User).filter(models.User.email == email)

    if query.first():
        #create a token
        access_token = oauth2.create_access_token(data = {"user_id": query.first().id})

        # return token
        return {"access_token": access_token, "token_type":"bearer"}

    else:
        verification_code = random.randint(100000, 999999)
        new_uza =  models.User(verification_code = verification_code, email = email, password="password", firstname = firstname, lastname = lastname, email_verified = 1)
        db.add(new_uza)
        db.commit()
        db.refresh(new_uza)

        #create a token
        access_token = oauth2.create_access_token(data = {"user_id": new_uza.id})

        # return token
        return {"id": new_uza.id, "email": new_uza.email, "access_token": access_token, "token_type":"bearer"}


