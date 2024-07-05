from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from logging import basicConfig, INFO
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Товары'),
    types.KeyboardButton("Заказать"),
    types.KeyboardButton("Контакты"),
]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

order_data = {}


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}!",
                         reply_markup=start_keyboard)


@dp.message_handler(text="О нас")
async def about_us(message: types.Message):
    await message.reply("Tehno-shop - Это магазин смартфонов. Мы открылись в 2024г в городе Ош. В нашем магазине вы можете приобрести смартфон любой модели: iPhone, Samsung, Redmi и другие")

@dp.message_handler(text="Контакты")
async def contact(message:types.Message):
    await message.answer(f'{message.from_user.full_name}, наши контакты:')
    await message.answer_contact("+996507912424", 'Zalkar', 'Anapiyaev')

Phone_buttons = [
    types.KeyboardButton("Samsung"),
    types.KeyboardButton("Iphone"),
    types.KeyboardButton("Huawei"),
    types.KeyboardButton("Назад")
]

Phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*Phone_buttons)


@dp.message_handler(text="Товары")
async def products(message: types.Message):
    await message.answer("Вот наши товары", reply_markup=Phone_keyboard)


@dp.message_handler(text="Samsung")
async def show_samsung(message: types.Message):
    await message.answer_photo("https://i1.wp.com/techshop.kg/wp-content/uploads/2018/09/2521c06e93b1ef86aea190649f2ffe3b_3_1-1000x1000.jpg?resize=768%2C768&ssl=1")
    await message.answer("Samsung-Galaxy A8\nЦена:21,200 сом\nАртикул - 33\nПамять - 1tb\nЦвет:черный")


@dp.message_handler(text="Iphone")
async def show_iphone(message: types.Message):
    await message.answer_photo("https://i0.wp.com/techshop.kg/wp-content/uploads/2018/12/52979-big.jpg?resize=300%2C300&ssl=1")
    await message.answer("iPhone-Xs Max\nена:93,160 сом\nАртикул - 55\nПамять:256tb\nЦвет:Белый")


@dp.message_handler(text="Huawei")
async def show_redmi(message: types.Message):
    await message.answer_photo("https://i0.wp.com/techshop.kg/wp-content/uploads/2018/08/huawei-p10-lite3-500x500.jpg?resize=500%2C500&ssl=1")
    await message.answer("Huawei -P10 Lite \nЦена:16,990 сом\nАртикул - 99\nПамять:32gb\nЦвет:черный")


@dp.message_handler(text="Назад")
async def back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=start_keyboard)
    
@dp.message_handler(text="Заказать")
async def order_product(message: types.Message):
    await message.answer("Пожалуйста, введите артикул товара, который хотите купить!")
    order_data[message.from_user.id] = {'step': 'waiting_for_articul'}

@dp.message_handler()
async def process_articul(message: types.Message):
    user_id = message.from_user.id
    if user_id in order_data and order_data[user_id]['step'] == 'waiting_for_articul':
        order_data[user_id]['articul'] = message.text
        order_data[user_id]['step'] = 'waiting_for_contact'
        await message.reply("Пожалуйста, поделитесь вашим контактом", 
                            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Поделиться контактом", request_contact=True)))

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    user_id = message.from_user.id
    if user_id in order_data and order_data[user_id]['step'] == 'waiting_for_contact':
        articul = order_data[user_id]['articul']
        contact = message.contact.phone_number
        user_name = message.contact.full_name

        order_message = (f"Новый заказ!\nАртикул: {articul}\nКонтакт: {contact}\nИмя: {user_name}")
        await bot.send_message(chat_id=-4107109022, text=order_message)
        await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.", reply_markup=start_keyboard)
        del order_data[user_id]



@dp.message_handler(text="Назад")
async def back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=start_keyboard)


executor.start_polling(dp, skip_updates=True)