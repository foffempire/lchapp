from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2_shorttime
from ..database import get_db
from sqlalchemy.orm import Session 
from ..utils import  baseURL, get_password_hash
import random
from ..email import send_mail

router = APIRouter(
    tags=["Reset Password"]
)


# ***************RESET PASSWORD*******************
@router.post("/resetpassword/")
async def reset_password(email: schemas.ResetPassword, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == email.email)
    if query.first():

        verification_code = random.randint(100000, 999999)
        query.first().verification_code = verification_code
        db.commit()
    
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
                        <img src='{baseURL}resources/images/logo.png' alt='logo' style='width:  250px;' />
                    </div>
                    <div style='padding-top: 20px;'>
                        <p>
                            We've received a request to reset your password. Here's the reset code;
                        </p>
                        <h4 style='background-color: #ffd7d7; padding: 10px; width: fit-content;'>
                            {verification_code}
                        </h4>
                        <p>
                            If you didn't make the request, just ignore this message. Password reset link is only valid for 10 minutes
                        </p>
                        <p>
                            if you have any questions, please email us at support@labourch.com, we can answer questions about your account.
                        </p>
                    </div>
                </div>
            </body>
            </html>
        """

        await send_mail(email.email, "Password reset", html)
        return {"data", "Check your email to reset your password"}
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Email not found!")



# ***************VERIFY RESET CODE*******************
@router.post("/verifyresetcode/{email}")
async def verify_reset_code(code: int, email: str, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == email, models.User.verification_code == code)
    if query.first():
        query.first().verification_code = 111111
        db.commit()
        return {"data", "success"}
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Verification failed!")




# ***************RESET PASSWORD*******************
@router.put("/setnewpassword/")
def create_password(newpass: schemas.VerifyResetPassword, db: Session = Depends(get_db)):
    
    # check password length
    if(len(newpass.password) < 6):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password length must be six characters or more")

    # check if password match
    if(newpass.password != newpass.confirm_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Passwords doesn't match")
    
    #check if user is in the database
    query = db.query(models.User).filter(models.User.email == newpass.email, models.User.verification_code == 111111)
    if query.first():
        npass = get_password_hash(newpass.password)
        query.first().password = npass
        query.first().verification_code = 100001
        db.commit()

        return {"data":"success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed! Try again")



# ***************RESEND CODE*******************
@router.post("/resendemail/{email}")
async def resend_email(email: str, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == email)
    if query.first():

        verification_code = random.randint(100000, 999999)
        query.first().verification_code = verification_code
        db.commit()

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
                        <img src='{baseURL}resources/images/logo.png' alt='logo' style='width:  250px;' />
                    </div>
                    <div style='padding-top: 20px;'>
                        <p>
                            We've received a request to reset your password. Here's the reset code;
                        </p>
                        <h4 style='background-color: #ffd7d7; padding: 10px; width: fit-content;'>
                            {verification_code}
                        </h4>
                        <p>
                            If you didn't make the request, just ignore this message. Password reset link is only valid for 10 minutes
                        </p>
                        <p>
                            if you have any questions, please email us at support@labourch.com, we can answer questions about your account.
                        </p>
                    </div>
                </div>
            </body>
            </html>
        """

        await send_mail(email, "Password reset", html)

        return {"data", "success"}
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Email not found!")