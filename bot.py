from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="7371249679:AAGRkXzHIpJHHAaDhKxULM7iP7q8LqEw2iA")
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer("Привет!\nЯ твой личный помощник")
    
@dp.message_handler(commands="help")
async def help(message:types.Message):
    await message.reply("Чем могу помочь?")
    
executor.start_polling(dp, skip_updates=True)