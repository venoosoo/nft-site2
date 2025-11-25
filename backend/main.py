from fastapi import FastAPI, Request
import hashlib
import hmac
import time

app = FastAPI()

BOT_TOKEN = "8025400265:AAHm47VJpa30QPBvlMvWOeEdfH1JdMpytNw"

def check_telegram_auth(data: dict) -> bool:
    """Validates Telegram Login Widget auth."""
    auth_hash = data.pop("hash", None)
    sorted_data = sorted([f"{k}={v}" for k, v in data.items()])
    data_check_string = "\n".join(sorted_data)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return calculated_hash == auth_hash

@app.post("/telegram-auth")
async def telegram_auth(request: Request):
    body = await request.json()

    if not check_telegram_auth(body.copy()):
        return {"ok": False, "reason": "invalid_hash"}

    # If the user allowed phone number
    phone = body.get("phone_number", None)

    return {
        "ok": True,
        "user": body,
        "phone_received": phone is not None,
        "phone": phone
    }
