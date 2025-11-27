# bot_print_contact.py
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from db_func import add_user_id_and_phone
import aiohttp
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8025400265:AAHm47VJpa30QPBvlMvWOeEdfH1JdMpytNw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Please share your phone number:", reply_markup=reply_markup)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        logger.info("Contact handler triggered but no contact found in update.")
        await update.message.reply_text("No contact found.")
        return

    # PRINT phone to console
    print(f"[BOT] Received contact — telegram_id={contact.user_id}, phone={contact.phone_number}")
    add_user_id_and_phone(contact.user_id,contact.phone_number)




def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Starting bot (polling). Open Telegram and send /start to the bot.")
    app.run_polling()

if __name__ == "__main__":
    main()
