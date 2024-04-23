from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 
import firebase_admin
from firebase_admin import credentials


router = APIRouter(
    tags=['Admin Notificaton']
)



# ***************ADD NOTIFICATIONS*******************
@router.post("/notify", status_code=status.HTTP_200_OK, response_model=schemas.NotificationResponse)
def notify(notify: schemas.Notification, db: Session = Depends(get_db), admin_user: str = Depends(oauth2_admin.get_admin_user)):
    insert = models.Notification(**notify.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)

    return insert



# **********************PUSH NOTIFICATION*******************

# import app.FCMmanager as fcm

# tokens = ["dY-f_WAfQ8erWRA1ZgnKTd:APA91bGUfgvDrmeBn_7vpu0aaOpLuHIngk-1c8JygoIjnvix9fbKTm3yp99T9zL1i-vfTSp"
#           "-7Zv69pZokrdtpBswD1AKNUKcc_mqvemVY_ItC-WffgzWRfyMoMjbOSG6KSy7_Bui93a3"]
# fcm.sendPush("Hi", "This is my next msg", tokens)