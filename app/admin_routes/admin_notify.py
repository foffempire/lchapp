from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session 


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


