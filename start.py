from aiogram import types, Dispatcher
from create_bot import bot, USERS
from keyboards import get_main_keyboard


async def start_handler(message: types.Message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    await bot.send_message(chat_id, "Hey, it's spf-bot.", reply_markup=await get_main_keyboard(user_id))
