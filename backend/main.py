# main.py
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8025400265:AAHm47VJpa30QPBvlMvWOeEdfH1JdMpytNw"
BACKEND_URL = "http://127.0.0.1:8000/phone"  # Ensure this is reachable from bot

# --- FastAPI backend ---
app = FastAPI()

class PhoneNumber(BaseModel):
    user_id: int
    phone_number: str

@app.post("/phone")
async def receive_phone(data: PhoneNumber):
    print(f"[BACKEND] Received phone from user {data.user_id}: {data.phone_number}")
    return {"status": "ok"}

# --- Telegram bot handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Please share your phone number:", reply_markup=reply_markup)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("No contact received.")
        return

    print(f"[BOT] Received contact: user_id={contact.user_id}, phone_number={contact.phone_number}")

    # Send phone to backend
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                BACKEND_URL,
                json={"user_id": contact.user_id, "phone_number": contact.phone_number},
                timeout=10
            )
        print(f"[BOT] Backend responded: {resp.status_code}, {resp.text}")
    except Exception as e:
        print(f"[BOT] Failed to send to backend: {e}")

    await update.message.reply_text("Thanks! Your phone number has been sent.")

# --- Run both FastAPI and Telegram bot together ---
async def main():
    # Setup bot
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    # Start bot polling in background
    bot_task = asyncio.create_task(bot_app.run_polling())

    # Start FastAPI
    import uvicorn
    api_task = asyncio.create_task(
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    )

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())
