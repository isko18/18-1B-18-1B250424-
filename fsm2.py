import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import token
from database import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('sql.db')
db.create_table()

class Form(StatesGroup):
    username = State()

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await Form.username.set()
    await message.reply("Привет! Как тебя зовут?")

@dp.message_handler(state=Form.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    db.add_user(message.from_user.id, username)
    await state.finish()
    await message.reply(f"Приятно познакомиться, {username}!")

@dp.message_handler(Command('me'))
async def me(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user:
        await message.reply(f"Ты зарегистрирован как {user[2]}")
    else:
        await message.reply("Ты еще не зарегистрирован")
        # await start(message)

async def on_startup(dp):
    logging.info("Настройки базы")
    db.create_table()
    logging.info("База загружена")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
