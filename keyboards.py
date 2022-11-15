from aiogram import types
from create_bot import ADMINS, SPECIALTIES, GRADES, GROUPS

####KEYBOARDS
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Create room', 'Delete room')
user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Find room', 'Edit info')
single_cross_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('❌')
cross_and_previous_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('❌', '👈')
specialties_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
grades_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
groups_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
####KEYBOARDS


for i in SPECIALTIES:
    specialties_keyboard.add(i)
for k in GRADES:
    grades_keyboard.add(k)
for j in GROUPS:
    groups_keyboard.add(j)

specialties_keyboard.add('👈', '❌')
grades_keyboard.add('👈', '❌')
groups_keyboard.add('👈', '❌')


async def get_keyboard(user_id, state): ### state = Class:state
    state_str = state.split(':')[1]

    if state_str == 'full_name':
        return single_cross_keyboard
    elif state_str == 'sex':
        return cross_and_previous_keyboard
    elif state_str == 'speciality':
        return specialties_keyboard
    elif state_str == 'grade':
        return grades_keyboard
    elif state_str == 'group':
        return groups_keyboard


async def get_main_keyboard(user_id):
    if user_id in ADMINS:
        return admin_keyboard
    else:
        return user_keyboard

