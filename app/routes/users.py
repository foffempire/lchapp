from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session 
from ..utils import get_password_hash, verify_password, baseURL, generate_unique_id
from fastapi.responses import JSONResponse
import shutil
import os
from ..email import send_mail
import random
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["User"]
)

# userImgUrl = f"{baseURL}uploads/users/"
userImgUrl = "uploads/users/"

# Jinja2 templating
templates = Jinja2Templates(directory="templates")


@router.get("/")
def root():
    return RedirectResponse('https://www.labourch.com', status_code=status.HTTP_302_FOUND, headers={"x-error": "Invalid credentials"})



# ***************REGISTER USER******************
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: schemas.RegisterUser, db: Session = Depends(get_db)):
    user.email = user.email.lower()
    #email exist
    email_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exist in our database")
    
    # check password length
    if(len(user.password) < 6):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password length must be six characters or more")
        

    verification_code = random.randint(100000, 999999)
    fake_code = generate_unique_id(25)
    user.password = get_password_hash(user.password)

    new_uza =  models.User(verification_code = verification_code, **user.model_dump())
    db.add(new_uza)
    db.commit()
    db.refresh(new_uza)

    # send welcome email
    html = f"""\
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap" rel="stylesheet">
        <title>Labour Connect Hub</title>
    </head>
    <body style='background-color: #f5f5f5; width: 100%;font-family: Roboto, sans-serif; font-size: 14px;color: #525252; letter-spacing: 0.5px;'>
        <div style='max-width: 600px; padding: 30px; margin: auto;'>
            <div style='background-color: #fff; padding: 30px;'>
                <img src='{baseURL}resources/images/logo.png' alt='logo' style='width:200px;' />
            </div>
            <div style='padding-top: 20px;'>
                <p>
                    Welcome to Labour Connect Hub, to get started click the link below to confirm your email.
                </p>
                <div style="padding: 20px 0;">
                    <a style='background-color: #ffd7d7; padding: 10px 20px; width: fit-content;color: #d60505; text-decoration: none;' href="{baseURL}register/{user.email}/{verification_code}/{fake_code}">Confirm email</a>
                </div>
                <p>
                    if you have any questions, please email us at support@labourch.com, we can answer questions about your account.
                </p>
            </div>
        </div>
    </body>
    </html>
"""

    await send_mail(user.email, "Confirm your email", html)
    
    #create a token
    access_token = oauth2.create_access_token(data = {"user_id": new_uza.id})

    # return token
    return {"id": new_uza.id, "email": new_uza.email, "access_token": access_token, "token_type":"bearer"}
    # return new_uza


# ***************RESEND CONFIRMATION EMAIL******************
@router.post("/resend/{email}", status_code=status.HTTP_201_CREATED)
async def resend(email: str, db: Session = Depends(get_db)):
    email = email.lower()

    query = db.query(models.User).filter(models.User.email == email).first()
    if query:
        verification_code = random.randint(100000, 999999)
        fake_code = generate_unique_id(25)

        query.verification_code = verification_code
        db.commit()

        # send welcome email
        html = f"""\
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap" rel="stylesheet">
            <title>Labour Connect Hub</title>
        </head>
        <body style='background-color: #f5f5f5; width: 100%;font-family: Roboto, sans-serif; font-size: 14px;color: #525252; letter-spacing: 0.5px;'>
            <div style='max-width: 600px; padding: 30px; margin: auto;'>
                <div style='background-color: #fff; padding: 30px;'>
                    <img src='{baseURL}resources/images/logo.png' alt='logo' style='width:200px;' />
                </div>
                <div style='padding-top: 20px;'>
                    <p>
                        Welcome to Labour Connect Hub, to get started click the link below to confirm your email.
                    </p>
                    <div style="padding: 20px 0;">
                        <a style='background-color: #ffd7d7; padding: 10px 20px; width: fit-content;color: #d60505; text-decoration: none;' href="{baseURL}register/{email}/{verification_code}/{fake_code}">Confirm email</a>
                    </div>
                    <p>
                        if you have any questions, please email us at support@labourch.com, we can answer questions about your account.
                    </p>
                </div>
            </div>
        </body>
        </html>
    """

        await send_mail(email, "Confirm your email", html)
        
        return {"data": f"Email sent to {email}"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found in our database")


# ***************EMAIL CONFIRMATION******************
@router.get("/register/{email}/{verify}/{code}", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
def verify_email(email: str, verify: int, request: Request, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == email, models.User.verification_code == verify)

    # if email and code not found
    if not query.first():
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Verification failed! Email not found, or already verified.")
        return templates.TemplateResponse(request=request, name="verification_failed.html", context={"baseURL": baseURL})

    # if email and code is found
    if query.first():
        query.first().verification_code = 100001
        query.first().email_verified = 1
        db.commit()
        # return {"data":"success"}

        return templates.TemplateResponse(request=request, name="verification_success.html", context={"baseURL": baseURL})


# ***************PHONE CONFIRMATION******************
@router.post("/user/phone/", status_code=status.HTTP_201_CREATED)
def verify_phone(ph: schemas.VerifyPhone, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.phone == ph.phone, models.User.verification_code == ph.code)

    # if phone and code not found
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Verification failed! Phone number not found, or already verified.")

    # if phone and code is found
    if query.first():
        query.first().verification_code = 100001
        query.first().phone_verified = 1
        db.commit()
        return {"data":"success"}


# ***************PERSONAL DETAILS*******************
@router.post("/user/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_personal_details(user: schemas.Personal, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == current_user.id)
    
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(user.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/user/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_personal_detail(user: schemas.Personal, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == current_user.id)
    
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(user.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

# ***************UPDATE PASSWORD*******************
@router.post("/user/password/", status_code=status.HTTP_202_ACCEPTED)
def update_password(user: schemas.Password, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    # check password length
    if(len(user.password) < 6):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password length must be six characters or more")
    
    # hash the password
    user.password = get_password_hash(user.password)

    
    #check if user exist
    query = db.query(models.User).filter(models.User.id == current_user.id)
    user_exist = query.first()
    if user_exist:
        # verify if old paswword is correct
        verfy_pass = verify_password(user.old_password, user_exist.password)
        if not verfy_pass:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")

        query.update({"password": user.password}, synchronize_session=False)
        db.commit()
        return {"data": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User doesn't exist")
    

# ***************UPLOAD USER IMAGE*******************
@router.post("/user/upload/")
def upload_user_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/users/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"

    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : userImgUrl+filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
 

# ***************UPDATE IMAGE*******************
@router.post("/user/image/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_personal_image(img: schemas.PersonalImg, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == current_user.id)
    
    #details exist
    details_exist = query.first()
    if details_exist:
        query.update(img.model_dump(), synchronize_session=False)
        db.commit()
        return query.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



# ***************GET USER DETAILS*******************
@router.get("/user/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_personal_details(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    results =  db.query(models.User).filter(current_user.id == models.User.id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No personal details found.")
    
    return results



# ***************DELETE ACCOUNT*******************
@router.get("/user/deleteaccount", status_code=status.HTTP_200_OK)
def delete_account(request: Request):

    return templates.TemplateResponse(request=request, name="delete_account.html")