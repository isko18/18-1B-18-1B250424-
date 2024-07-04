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


Phone_buttons = [
    types.KeyboardButton("Samsung"),
    types.KeyboardButton("Iphone"),
    types.KeyboardButton("Redmi"),
    types.KeyboardButton("Poco"),
    types.KeyboardButton("Назад")
]

Phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*Phone_buttons)


@dp.message_handler(text="Товары")
async def products(message: types.Message):
    await message.answer("Вот наши товары", reply_markup=Phone_keyboard)


@dp.message_handler(text="Samsung")
async def show_samsung(message: types.Message):
    await message.answer_photo("https://ekt.stores-apple.com/upload/iblock/9df/tjwlqyhgd8jmive2hw9ypdzxgnn72p5a.jpg")
    await message.answer("Samsung - s24 ultra\nЦена - 80000\nАртикул - 13\nПамять - 1tb\nЦвет: черный")


@dp.message_handler(text="Iphone")
async def show_iphone(message: types.Message):
    await message.answer_photo("https://www.vgadz.com/wp-content/uploads/2023/10/Idol_Magsafe_Black_iPhone15ProMax_BlueTitanium_FrontBack.webp")
    await message.answer("Iphone - 15 pro max\nЦена - 100000\nАртикул - 15\nПамять - 1tb\nЦвет: Титан")


@dp.message_handler(text="Redmi")
async def show_redmi(message: types.Message):
    await message.answer_photo("https://mistore.kg/wp-content/uploads/2024/01/xiaomi-redmi-note-13-pro-plus_black.jpg")
    await message.answer("Redmi - not 13 pro\nЦена - 20000\nАртикул - 10\nПамять - 256gb\nЦвет: черный")


@dp.message_handler(text="Poco")
async def show_poco(message: types.Message):
    await message.answer_photo("https://softech.kg/image/cache/508ac048a1c0786ecdcf2d0941007fcb.jpg")
    await message.answer("Poco - x6 pro\nЦена - 15000\nАртикул - 18\nПамять - 256gb\nЦвет: Желтый")



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

        order_message = f"Новый заказ!\nАртикул: {articul}\nКонтакт: {contact}\nИмя: {user_name}"
        
        await bot.send_message(chat_id=-4107109022, text=order_message)

        await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.", reply_markup=start_keyboard)
        del order_data[user_id]


@dp.message_handler(text="Контакты")
async def contact_info(message: types.Message):
    await message.reply(f'{message.from_user.full_name}, Вот наши контакты:')
    await message.answer_contact("+996551519651", 'Azamkhodja', 'Saydabarov')


@dp.message_handler(text="Назад")
async def back(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=start_keyboard)


executor.start_polling(dp, skip_updates=True)
