from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, SPECIALTIES, GRADES, GROUPS, USERS
from keyboards import single_cross_keyboard, get_main_keyboard, specialties_keyboard, grades_keyboard, groups_keyboard, cross_and_previous_keyboard
from aiogram.dispatcher.filters import Text
from database import update_or_create_user, get_user


class Form(StatesGroup):
    full_name = State()
    sex = State()
    speciality = State()
    grade = State()
    group = State()


MESSAGES_FOREACH_STATE = {Form.full_name.state: {'message': 'Enter your full name. Format: Name Surname:', 'reply_markup': single_cross_keyboard},
                          Form.sex.state: {'message': 'Enter your sex', 'reply_markup': cross_and_previous_keyboard},
                          Form.speciality.state: {'message': 'Enter your speciality', 'reply_markup': specialties_keyboard},
                          Form.grade.state: {'message': 'Enter your grade', 'reply_markup': grades_keyboard},
                          Form.group.state: {'message': 'Enter your group', 'reply_markup': groups_keyboard}}


async def send_message(state, chat_id):
    msg = MESSAGES_FOREACH_STATE[state]['message']
    reply_markup = MESSAGES_FOREACH_STATE[state]['reply_markup']
    await bot.send_message(chat_id, msg, reply_markup=reply_markup)

###CHECK DATA, IF CORRECT - RETURN###
async def full_name(message_text):
    # user_name_str = message_text
    user_name = message_text.split(' ')
    if len(user_name) != 2 or not all(c.isalpha() or c.isspace() for c in message_text):
        return None
    else:
        return message_text


async def sex(message_text):
    if message_text.lower() == 'male' or message_text.lower() == 'female':
        return message_text.lower()
    return None


async def speciality(message_text):
    if message_text.lower() not in SPECIALTIES:
        return None
    else:
        return message_text.lower()


async def grade(message_text):
    if message_text.lower() not in GRADES:
        return None
    else:
        return message_text.lower()


async def group(message_text):
    if message_text.lower() not in GROUPS:
        return None
    else:
        return message_text.lower()
###CHECK DATA, IF CORRECT - RETURN###


async def previous_handler(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    current_state = await state.get_state()

    if current_state is None:
        return

    for i in Form.states_names:
        if current_state == i:
            previous_state = await Form.previous()
            if previous_state is None:
                await bot.send_message(chat_id, "Cancel.", reply_markup=await get_main_keyboard(user_id))
                await state.finish()
                return
            await state.set_state(previous_state)
            msg = MESSAGES_FOREACH_STATE[previous_state]['message']
            reply_markup = MESSAGES_FOREACH_STATE[previous_state]['reply_markup']
            await bot.send_message(chat_id, msg, reply_markup=reply_markup)


async def start_register(message: types.Message):
    chat_id = str(message.chat.id)
    if await get_user(str(message.from_user.id)):
        await bot.send_message(chat_id, 'You are registered user.')
        return

    await bot.send_message(chat_id, 'Enter your full name. Format: Name Surname(no digits or any special symbols)',
                           reply_markup=single_cross_keyboard)
    await Form.full_name.set()


async def full_name_handler(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_full_name = await full_name(message.text)

    if user_full_name is None:
        await bot.send_message(chat_id, 'Incorrect format.')

    else:
        await send_message(Form.sex.state, chat_id)
        await state.update_data(full_name=user_full_name)

        await Form.next() ###change state to sex


async def sex_handler(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_sex = await sex(message.text)

    if user_sex is None:
        await bot.send_message(chat_id, 'Incorrect sex. Enter: female or male.')

    else:
        await send_message(Form.speciality.state, chat_id)
        await state.update_data(sex=user_sex)

        await Form.next() ###change state to speciality


async def speciality_handler(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_speciality = await speciality(message.text)
    if user_speciality is None:
        await bot.send_message(chat_id, 'Not-existent speciality')
    else:
        await send_message(Form.grade.state, chat_id)
        await state.update_data(speciality=message.text.lower())

        await Form.next() ###change to grade


async def grade_handler(message: types.Message, state: FSMContext):
    chat_id = str(message.chat.id)
    user_grade = await grade(message.text)
    if user_grade is None:
        await bot.send_message(chat_id, 'Not-existent grade')
    else:
        await send_message(Form.group.state, chat_id)
        await state.update_data(grade=message.text.lower())

        await Form.next() ###change state to group


async def group_handler(message: types.Message, state:FSMContext):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    group_str = await group(message.text)
    if group_str is None:
        await bot.send_message(chat_id, "Not-existent group")
    else:
        await bot.send_message(chat_id, "Nice! Now you can find some people to talk.",
                               reply_markup=await get_main_keyboard(user_id))

        async with state.proxy() as data:
            user_id = str(message.from_user.id)
            full_name = data['full_name']
            sex = data['sex']
            speciality = data['speciality']
            grade = data['grade']
            user_group = message.text.lower()

        data = (user_id, full_name, sex, speciality, grade, user_group, 0)

        USERS[user_id] = {'full_name': full_name, 'sex': sex,
                          'speciality': speciality, 'grade': grade,
                          'group': user_group, 'meetings_counter': 0}

        await update_or_create_user(data) ###create user in db
        await state.finish() ### finish state


async def start_change(message: types.Message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if not await get_user(user_id):
        await bot.send_message(chat_id, "You're not registered yet.")
        return

    user = await get_user(user_id)
    await send_message(Form.full_name.state, chat_id)

    await Form.full_name.set()


def register_handlers(dp: Dispatcher):
    ###COMMANDS###
    dp.register_message_handler(start_register, commands=['register'], chat_type=[types.ChatType.PRIVATE])
    dp.register_message_handler(start_change, commands=['change'], chat_type=[types.ChatType.PRIVATE])
    ###COMMANDS###

    dp.register_message_handler(previous_handler, Text(equals=['👈']), state=Form.states_names)

    ###STATES HANDLERS###
    dp.register_message_handler(full_name_handler, state=Form.full_name)
    dp.register_message_handler(sex_handler, state=Form.sex)
    dp.register_message_handler(speciality_handler, state=Form.speciality)
    dp.register_message_handler(grade_handler, state=Form.grade)
    dp.register_message_handler(group_handler, state=Form.group)
    ###STATES HANDLERS###
