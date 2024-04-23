from .. import FCMmanager as fcm
from fastapi import APIRouter
from typing import List

router = APIRouter(
    tags=['Push notification']
)



# **********************PUSH NOTIFICATION*******************
@router.post("/send_push_notification/")
async def send_push_notification(title: str, msg: str, device_token: str):
    fcm.sendPush(title, msg, device_token)

