import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils import executor

from database import Database

API_TOKEN = 'YOUR_BOT_API_TOKEN'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database('database.db')
db.create_table()

class Form(StatesGroup):
    username = State()

@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.username)
    await message.reply("Привет! Как тебя зовут?")

@dp.message(Form.username)
async def process_username(message: Message, state: FSMContext):
    username = message.text
    db.add_user(message.from_user.id, username)
    await state.clear()
    await message.reply(f"Приятно познакомиться, {username}!")

@dp.message(Command('me'))
async def cmd_me(message: Message):
    user = db.get_user(message.from_user.id)
    if user:
        await message.reply(f"Ты зарегистрирован как {user[2]}")
    else:
        await message.reply("Ты еще не зарегистрирован.")

async def on_startup(dp: Dispatcher):
    logging.info("Setting up the database...")
    db.create_table()
    logging.info("Database setup completed.")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
