from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()

ADMINS = []
USERS = {'1234': {'sex': 'female', 'grade': '1(бакалавр)', 'speciality': 'інженерія програмного забезпечення', 'user_group': 'іпс-12'},
         '123456': {'sex': 'female', 'grade': '1(бакалавр)', 'speciality': 'інженерія програмного забезпечення', 'user_group': 'іпс-11'},
         '879794826': {'sex': 'female', 'grade': '2(бакалавр)', 'speciality': 'прикладна математика', 'user_group': 'к-15'},
         '12345': {'sex': 'female', 'grade': '2(бакалавр)', 'speciality': 'прикладна математика', 'user_group': 'к-15'},
         }

queue = {'1234', '123456'}
on_meeting = {}

SPECIALTIES = ["прикладна математика", "інженерія програмного забезпечення", "комп'ютерні науки", "системний аналіз"]
GRADES = ['1(бакалавр)', '2(бакалавр)', '3(бакалавр)', '4(бакалавр)', '1(магістр)', '2(магістр)']
GROUPS = ['іпс-12', 'к-10', 'іпс-11', 'к-12']


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
