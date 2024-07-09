import logging
from aiogram import Bot, Dispatcher, types ,executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import token
import sqlite3


logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class Form(StatesGroup):
    first_name = State()
    last_name = State()
    username = State()
    direction = State()
    number = State()


def create_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            direction TEXT,
            number TEXT
        )
    ''')
    conn.commit()
    conn.close()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.first_name.set()
    await message.reply("Привет! Давайте запишем вас на DemoDay. Как вас зовут? (Имя)")

@dp.message_handler(state=Form.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await Form.next()
    await message.reply("Введите вашу фамилию:")

@dp.message_handler(state=Form.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await Form.next()
    await message.reply("Введите ваш никнейм (username):")

@dp.message_handler(state=Form.username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await Form.next()
    await message.reply("Введите ваше направление:")

@dp.message_handler(state=Form.direction)
async def process_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await Form.next()
    await message.reply("Введите ваш номер телефона:")

@dp.message_handler(state=Form.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
        
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (first_name, last_name, username, direction, number)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['first_name'], data['last_name'], data['username'], data['direction'], data['number']))
        conn.commit()
        conn.close()

        await message.reply("Вы успешно зарегистрированы на DemoDay!")
        await state.finish()
        
create_db()
executor.start_polling(dp, skip_updates=True)