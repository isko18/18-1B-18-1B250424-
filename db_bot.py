from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, sqlite3, time


from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    
    created VARCHAR(100)
);
""")

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f'SELECT id FROM users WHERE id = {message.from_user.id};')
    users_result = cursor.fetchall()
    print(users_result)
    if users_result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);",
                    (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, time.ctime()))
        cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}")
    
class MailingState(StatesGroup):
    text = State()
    
@dp.message_handler(commands='mailing')
async def start_mailing(message:types.Message):
    await message.answer("Напишите текст для рассылки: ")
    await MailingState.text.set()
    
    
@dp.message_handler(state=MailingState.text)
async def send_mailing(message:types.Message, state:FSMContext):
    await message.answer("Начинаю рассылку...")
    cursor.execute('SELECT id FROM users;')
    users_id = cursor.fetchall()
    for user_id in users_id:
        await bot.send_message(user_id[0], message.text)
    await message.answer("Рассылка окончена...")
    await state.finish()
    
@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял")
    
    
executor.start_polling(dp, skip_updates=True)

