# from .. import FCMmanager as fcm
from fastapi import APIRouter
from typing import List
import firebase_admin
from firebase_admin import credentials, messaging

router = APIRouter(
    tags=['Push notification']
)



# **********************PUSH NOTIFICATION*******************
@router.post("/send_push_notification/")
async def send_push_notification(device_token: str, title:str, message:str):
    cred = credentials.Certificate("./resources/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    # Create a message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message
        ),
        token=device_token,
    )

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)


