from aiogram import executor
from create_bot import dp
from register import register_handlers
from database import get_all_users
from find_partner import register_meet_handlers
from main_handlers import register_main_handlers


async def on_startup(_):
    print('Online')
    register_meet_handlers(dp)
    register_main_handlers(dp)
    register_handlers(dp)

    get_all_users()  ###append to USERS

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)