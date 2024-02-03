from fastapi import APIRouter, HTTPException, Depends, status, UploadFile
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List
from sqlalchemy import or_, desc, and_
from ..utils import generate_unique_id
from fastapi.responses import JSONResponse
import shutil
import os
from ..utils import baseURL
from datetime import datetime

router = APIRouter(
    tags=['messages']
)

# msgImgUrl = f"{baseURL}uploads/messages/"
msgImgUrl = "uploads/messages/"

def verify_owner(conversation_id, user_id, db):    
    msg = db.query(models.Conversations).filter(models.Conversations.id == conversation_id).first()
    if user_id == msg.sender_id:
        return True
    elif user_id == msg.receiver_id:
        return True
    else:
        return False


# ***************UPLOAD MESSAGE IMAGE*******************
@router.post("/message/upload/")
def upload_message_image(file: UploadFile ):

    # Define the directory to save uploaded images
    UPLOAD_DIRECTORY = "uploads/messages/"

    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename for the uploaded image
    file_extension = file.filename.split(".")[-1]
    filename = f"{utils.generate_unique_id(15)}.{file_extension}"
    
    
    try:
        # Save the uploaded file to the specified directory
        with open(os.path.join(UPLOAD_DIRECTORY+filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename" : msgImgUrl+filename}
    
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload file: {str(e)}"}, status_code=500)
 

# ***************ADD Message*******************
@router.post("/message/{receiver_id}", status_code=status.HTTP_200_OK, response_model=schemas.MessageResponse)
def send_message(receiver_id: int, msg: schemas.Message, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):


    if receiver_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="you Cannot send a message to yourself")

    updateTime = datetime.now()
    if not current_user.firstname:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Update your firstname and lastname to send a message")
    
    # check if there's conversation btw the sender and receiver
    query = db.query(models.Conversations).filter(or_(and_(models.Conversations.receiver_id == receiver_id, models.Conversations.sender_id == current_user.id),(and_(models.Conversations.sender_id == receiver_id, models.Conversations.receiver_id == current_user.id))))

    
    if query.first():
        conversation_id = query.first().id

        # update conversations table
        query.first().date_updated = updateTime
        query.first().last_message = msg.message
        db.commit()

        # insert into messages table
        insert = models.Messages(conversation_id = conversation_id, sender_id = current_user.id, **msg.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)


        return insert
    
    else:
        conversation_name = generate_unique_id(10) 

        # insert into conversation table   
        conv = models.Conversations(name = conversation_name, sender_id = current_user.id, receiver_id = receiver_id, last_message = msg.message, date_updated = updateTime)
        db.add(conv)
        db.commit()
        db.refresh(conv)

        stmt = db.query(models.Conversations).filter(models.Conversations.name == conversation_name)
        
        if stmt.first():
            # insert into messages table   
            insert = models.Messages(conversation_id = stmt.first().id,sender_id = current_user.id, **msg.model_dump())
            db.add(insert)
            db.commit()
            db.refresh(insert)
            return insert
    
        
@router.post("/reply_message/{conversation_id}", status_code=status.HTTP_200_OK, response_model=schemas.MessageResponse)
def reply_message(conversation_id: int, msg: schemas.Message, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    updateTime = datetime.now()
    if not current_user.firstname:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Update your firstname and lastname to send a message")
    
    # check if there's conversation btw the sender and receiver
    query = db.query(models.Conversations).filter(models.Conversations.id == conversation_id)

    
    if query.first():
        conversation_id = query.first().id

        # update conversations table
        query.first().date_updated = updateTime
        query.first().last_message = msg.message
        db.commit()
        
        # insert into messages table
        insert = models.Messages(conversation_id = conversation_id, sender_id = current_user.id, **msg.model_dump())
        db.add(insert)
        db.commit()
        db.refresh(insert)


        return insert
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Conversation with id of {conversation_id} was not found")
    

# ***************GET CONVERSATIONS*******************
@router.get('/message', status_code=status.HTTP_200_OK)
def get_my_conversations(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Conversations).filter(or_(models.Conversations.receiver_id == current_user.id, models.Conversations.sender_id == current_user.id)).order_by(desc(models.Conversations.date_updated)).all()
   
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No messages found")  
    
    # return query
    my_list=[]
    for chat in query:
        if chat.sender_id is not current_user.id:
            my_list.append({ "id": chat.id, "last_message": chat.last_message, "date_updated": chat.date_updated, "user": chat.sender_id})
        else:
            my_list.append({ "id": chat.id, "last_message": chat.last_message, "date_updated": chat.date_updated, "user": chat.receiver_id})
    
    return my_list
    
     

# ***************GET CONVERSATIONS USER*******************
@router.get('/message_user/{conversation_id}', status_code=status.HTTP_200_OK)
def get_convesation_user(conversation_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Conversations).filter(models.Conversations.id == conversation_id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No conversation with id of {conversation_id}") 
    
  
    if query.first().sender_id is not current_user.id:
        chat_with = query.first().sender_id
    else:
        chat_with = query.first().receiver_id
    
    stmt = db.query(models.User).filter(models.User.id == chat_with).first()

    if not stmt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found") 
    
    return {"firstname": stmt.firstname, "lastname": stmt.lastname, "image": stmt.image }
 
 

# ***************GET ONE MESSAGING*******************
@router.get('/message/{conversation_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.MessageResponse])
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Messages).filter(models.Messages.conversation_id == conversation_id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No conversation with id of {conversation_id}")  
    
    if not verify_owner(conversation_id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You not autorized to view this message {conversation_id}")  
     
    return query





