from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):
    pass


async def admin(message: types.Message):
    if message.text == '/addlink':
        pass
    elif message.text == '/rmlink':
        pass
    elif message.text == '':
        pass