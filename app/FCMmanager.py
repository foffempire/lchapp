import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("./resources/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_push_notification(device_token, title, message):
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