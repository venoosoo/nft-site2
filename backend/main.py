import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import httpx

BOT_TOKEN = "8025400265:AAHm47VJpa30QPBvlMvWOeEdfH1JdMpytNw"
BACKEND_URL = "http://localhost:8000/phone"

# --- FastAPI backend ---
app = FastAPI()

class PhoneNumber(BaseModel):
    user_id: int
    phone_number: str

@app.post("/phone")
async def receive_phone(data: PhoneNumber):
    print(f"Received phone from user {data.user_id}: {data.phone_number}")
    return {"status": "ok"}

# --- Telegram bot handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your phone number:", reply_markup=reply_markup)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        async with httpx.AsyncClient() as client:
            try:
                await client.post(BACKEND_URL, json={
                    "user_id": contact.user_id,
                    "phone_number": contact.phone_number
                })
            except Exception as e:
                print(f"Failed to send to backend: {e}")
        await update.message.reply_text("Thanks! Your phone number has been sent.")

# --- Run both bot and FastAPI ---
async def run_bot():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    await bot_app.run_polling()

async def run_api():
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(run_bot(), run_api())

if __name__ == "__main__":
    asyncio.run(main())
