import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.reply_buttons import choose_location_buttons, main_menu_buttons
from bot.buttons.text import from_tashkent, from_samarkand, taxi_text, taxi_text_kr, taxi_text_ru, back_main_menu, \
    back_main_menu_kr, back_main_menu_ru
from bot.dispatcher import dp, bot
from bot.handlers.send_mail_handler import groups


@dp.message_handler(Text(equals=[taxi_text, taxi_text_kr, taxi_text_ru]))
async def taxi_function(msg: types.Message, state: FSMContext):
    await state.set_state("location_taxi")
    await state.update_data(order_type='taxi')
    if msg.text == taxi_text:
        lang = "uz"
        text = "🛣 Qaysi yo'nalishda taksi buyurtma bermoqchisiz? ⬇️"
    elif msg.text == taxi_text_kr:
        lang = "kr"
        text = "🛣 Қайси йўналишда такси буюртма бермоқчисиз? ⬇️"
    else:
        lang = "ru"
        text = "🛣 Выберите направление для заказа такси ⬇️"

    await state.update_data(language=lang)
    await msg.answer(text, reply_markup=await choose_location_buttons(msg.text))


@dp.message_handler(Text(equals=[from_tashkent, from_samarkand]), state='location_taxi')
async def ask_passenger_count(msg: types.Message, state: FSMContext):
    address = 'tashkent-samarkand' if msg.text == from_tashkent else 'samarkand-tashkent'
    await state.update_data(address=address)
    await state.set_state("passenger_count")

    user_data = await state.get_data()
    lang = user_data.get("language", "uz")

    messages = {
        "uz": "🚖 Nechta yo'lovchi borligini tanlang (1 dan 4 gacha):",
        "kr": "🚖 Нечта йўловчи борлигини танланг (1 дан 4 гача):",
        "ru": "🚖 Выберите количество пассажиров (от 1 до 4):"
    }

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(KeyboardButton("1"), KeyboardButton("2"))
    keyboard.row(KeyboardButton("3"), KeyboardButton("4"))

    back_button_texts = {
        "uz": back_main_menu,
        "kr": back_main_menu_kr,
        "ru": back_main_menu_ru
    }

    keyboard.add(KeyboardButton(back_button_texts.get(lang, back_main_menu)))
    await msg.answer(messages[lang], reply_markup=keyboard)


@dp.message_handler(Text(equals=["1", "2", "3", "4"]), state='passenger_count')
async def ask_phone_number(msg: types.Message, state: FSMContext):
    await state.update_data(passenger_count=msg.text)
    await state.set_state("taxi_phone_number")

    user_data = await state.get_data()
    lang = user_data.get("language", "uz")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_texts = {
        "uz": "📞 Telefon raqamni yuborish",
        "kr": "📞 Телефон рақамни юбориш",
        "ru": "📞 Отправить номер телефона"
    }
    keyboard.add(KeyboardButton(btn_texts[lang], request_contact=True))

    messages = {
        "uz": "📞 Telefon raqamingizni quyidagi formatda yuboring yoki pastdagi tugma orqali ⬇️\n\nMisol: +998935365985",
        "kr": "📞 Телефон рақамингизни қуйидаги форматда юборинг ёки пастдаги тугма орқали ⬇️\n\nМисол: +998935365985",
        "ru": "📞 Отправьте свой номер телефона в формате ниже или воспользуйтесь кнопкой ниже ⬇️\n\nПример: +998935365985"
    }

    await msg.answer(messages[lang], reply_markup=keyboard)


async def process_taxi_order(msg: types.Message, phone_number: str, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "uz")

    messages = {
        "uz": f"✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanamiz!",
        "kr": f"✅ Буюртмангиз қабул қилинди! Тез орада сиз билан боғланамиз!",
        "ru": f"✅ Ваш заказ принят! Мы скоро с вами свяжемся!"
    }

    data = {
        "chat_id": str(msg.from_user.id),
        "full_name": msg.from_user.full_name,
        "offer_type": "passenger",
        "delivery_address": user_data.get("address"),
        "number_of_passengers": str(user_data.get("passenger_count")),
        "phone_number": phone_number
    }
    requests.post("http://127.0.0.1:8000/api/offers/create/", json=data)

    await msg.answer(messages[lang], reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()

    order_text = (
        f"🚕 Yangi taksi buyurtmasi!\n\n"
        f"®️ Username: {msg.from_user.username}\n"
        f"📍 Yo‘nalish: {user_data.get('address')}\n"
        f"👥 Yo‘lovchilar soni: {user_data.get('passenger_count')}\n"
        f"📞 Telefon: {phone_number}"
    )

    for group in groups:
        try:
            await bot.send_message(chat_id=group,
                                   text=order_text + f"\n👤 Yuboruvchi: [{msg.from_user.full_name}](tg://user?id={msg.from_user.id})",
                                   parse_mode="HTML")
        except Exception as e:
            print(f"Guruhga xabar yuborishda xatolik: {e}")


@dp.message_handler(state="taxi_phone_number", content_types=types.ContentType.CONTACT)
async def get_phone_number(msg: types.Message, state: FSMContext):
    await process_taxi_order(msg, msg.contact.phone_number, state)


@dp.message_handler(state="taxi_phone_number", content_types=types.ContentType.TEXT)
async def get_phone_number_text(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+") and msg.text[1:].isdigit() and len(msg.text) == 13:
        await process_taxi_order(msg, msg.text, state)
    else:
        user_data = await state.get_data()
        lang = user_data.get("language", "uz")

        error_messages = {
            "uz": "❌ Iltimos, to'g'ri telefon raqam kiriting yoki pastdagi tugmadan foydalaning.\n\nMisol: +998935365985",
            "kr": "❌ Илтимос, тўғри телефон рақам киритинг ёки пастдаги тугмадан фойдаланинг.\n\nМисол: +998935365985",
            "ru": "❌ Пожалуйста, введите правильный номер телефона или воспользуйтесь кнопкой.\n\nПример: +998935365985"
        }

        await msg.answer(error_messages[lang])
