# bot_forward.py
import logging
import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8025400265:AAHm47VJpa30QPBvlMvWOeEdfH1JdMpytNw"
# If local testing with ngrok, use the ngrok HTTPS URL:
BACKEND_URL = "https://08f77fecc2d9.ngrok-free.app/phone"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт"
    )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("No contact received.")
        return

    print(f"[BOT] Received contact: telegram_id={contact.user_id} phone={contact.phone_number}")

    # Forward to backend (async)
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(BACKEND_URL,
                                     json={"user_id": contact.user_id, "phone_number": contact.phone_number})
        print(f"[BOT] Forwarded to backend: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"[BOT] Failed to forward to backend: {e}")

    await update.message.reply_text(f"Thanks! Your phone number has been sent. your number: {contact.phone_number}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Starting bot (polling).")
    app.run_polling()

if __name__ == "__main__":
    main()
