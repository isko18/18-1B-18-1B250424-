from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, sqlite3

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('DemoDay.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    direction VARCHAR(111),         
    number VARCHAR(111)
);
""")

class UsersState(StatesGroup):
    first_name = State()
    last_name = State()
    username = State()
    direction = State()
    number = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    users_result = cursor.fetchall()
    if not users_result:
        await message.answer("Добро пожаловать! Давайте начнем процесс регистрации.\n"
                             "Введите ваше имя:")
        await UsersState.first_name.set()
    else:
        await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message_handler(state=UsersState.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await message.answer("Теперь введите вашу фамилию:")
    await UsersState.last_name.set()

@dp.message_handler(state=UsersState.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await message.answer("Введите ваш никнейм:")
    await UsersState.username.set() 

@dp.message_handler(state=UsersState.username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

    await message.answer("Введите ваш адрес:")
    await UsersState.direction.set()

@dp.message_handler(state=UsersState.direction)
async def process_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text

    await message.answer("Введите ваш номер телефона:")
    await UsersState.number.set() 

@dp.message_handler(state=UsersState.number)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text

        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);",
                       (message.from_user.id, data['first_name'], data['last_name'],
                        data['username'], data['direction'], data['number']))
        connection.commit()

        await message.answer("Спасибо за регистрацию! Вы успешно зарегистрированы.")
        await state.finish()  

@dp.message_handler()
async def start_mailing(message: types.Message):
    await message.reply("Извините, я вас не понял.")

executor.start_polling(dp, skip_updates=True)
