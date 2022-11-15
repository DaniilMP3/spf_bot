from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import get_main_keyboard
from aiogram.dispatcher.filters import Text


async def cancel_handler(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    current_state = await state.get_state()
    if current_state is None:
        return

    if message.text == '❌':
        await state.finish()
        await message.reply('Cancelled.', reply_markup=await get_main_keyboard(user_id))


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Text(equals=['❌']), state='*')