from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import or_, desc
from typing import List


router = APIRouter(
    tags=['Notifications']
)

# ***************ADD NOTIFICATIONS*******************
# @router.post("/notify", status_code=status.HTTP_200_OK, response_model=schemas.NotificationResponse)
# def notify(notify: schemas.Notification, db: Session = Depends(get_db)):
def notify(user_id: int, title: str, message:str, db: Session = Depends(get_db)):
    insert = models.Notification(user_id=user_id, title=title, message=message)
    db.add(insert)
    db.commit()
    db.refresh(insert)

    return insert

# ***************GET NOTIFICATIONS*******************
@router.get("/notifications", status_code=status.HTTP_200_OK, response_model=List[schemas.NotificationResponse])
def get_notification(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Notification).filter(or_(models.Notification.user_id == current_user.id, models.Notification.user_id == 0)).order_by(desc(models.Notification.date_created)).limit(5)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No notifications found!")
    return query.all()


# ***************COUNT UNREAD NOTIFICATIONS*******************
@router.get("/count_notification", status_code=status.HTTP_200_OK)
def count_unread_notification(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Notification).filter(or_(models.Notification.user_id == current_user.id, models.Notification.user_id == 0), models.Notification.is_read == 0)
    if not query.first():
        return 0
    else:
        return len(query.all())



# ***************MARK NOTIFICATION AS READ*******************
@router.put("/read_notify/{id}", status_code=status.HTTP_200_OK, response_model=schemas.NotificationResponse)
def mark_as_read(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Notification).filter(models.Notification.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    query.first().is_read = 1
    db.commit()

    return query.first()
