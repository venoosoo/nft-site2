# bot_print_contact.py
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from db_func import new_user, save_num_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8332162563:AAGFof_5kgK219tSrgcO6smD4rHldnewISw"

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await new_user(message.from_user.id)
    keyboard = [[KeyboardButton(text="Share phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Please share your phone number:", reply_markup=reply_markup)

@router.message(F.contact)
async def contact_handler(message: Message):
    contact = message.contact
    if not contact:
        logger.info("Contact handler triggered but no contact found in message.")
        await message.answer("No contact found.")
        return

    print(f"[BOT] Received contact — telegram_id={contact.user_id}, phone={contact.phone_number}")
    await save_num_user(message.from_user.id, contact.phone_number)
    await message.answer("Thank you! Your contact has been saved.")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)
    
    print("Starting bot (polling). Open Telegram and send /start to the bot.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())