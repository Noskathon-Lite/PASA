import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("/home/sandarva3/Documents/bettermind9749.json")
firebase_admin.initialize_app(cred)

def send_push_notification(fcm_token, title, body, data):
    """
    Send a push notification to a specific device using its FCM token.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data,  # Include additional data payload (e.g., channel_name, token)
        token=fcm_token
    )
    response = messaging.send(message)
    return response
