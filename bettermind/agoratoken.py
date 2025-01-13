from agora_token_builder import RtcTokenBuilder
import time

APP_ID = "YOUR_AGORA_APP_ID"
APP_CERTIFICATE = "YOUR_AGORA_APP_CERTIFICATE"

def generate_agora_token(channel_name, uid, role='publisher'):
    expiration_time_in_seconds = 3600  #valid for 1 hour
    current_time = int(time.time())
    privilege_expired_ts = current_time + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(
        APP_ID, APP_CERTIFICATE, channel_name, uid, role, privilege_expired_ts
    )
    return token
