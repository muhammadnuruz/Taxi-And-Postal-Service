import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.reply_buttons import choose_location_buttons, main_menu_buttons
from bot.buttons.text import be_driver, be_driver_kr, be_driver_ru, mail_text, mail_text_kr, from_tashkent, \
    from_samarkand, mail_text_ru
from bot.dispatcher import dp, bot

groups = [1974800905]


@dp.message_handler(Text(equals=[be_driver, be_driver_kr, be_driver_ru]))
async def be_driver_function(msg: types.Message):
    if msg.text == be_driver:
        await msg.answer(text="Taksi haydovchisi bo‘lishni xohlovchilar uchun taklif!\nMurojaat uchun: @Zuhriddin_774👇")
    elif msg.text == be_driver_kr:
        await msg.answer(text="Такси ҳайдовчиси бўлишни хоҳловчилар учун таклиф!\нМурожаат учун: @Zuhriddin_774👇")
    else:
        await msg.answer(text="Предложение для тех, кто хочет стать таксистом!\nДля подачи заявки: @Zuhriddin_774👇")


@dp.message_handler(Text(equals=[mail_text, mail_text_kr, mail_text_ru]))
async def mail_function(msg: types.Message, state: FSMContext):
    await state.set_state("location_mail")
    await state.update_data(offer_type='mail')
    if msg.text == mail_text:
        lang = "uz"
        text = "🛣 Qaysi yo'nalishda pochta jonatmoqchi ekanligizni tanlang ⬇️"
    elif msg.text == mail_text_kr:
        lang = "kr"
        text = "🛣 Қайси йўналишда почта жонатмоқчи эканлигизни танланг ⬇️"
    else:
        lang = "ru"
        text = "🛣 Выберите, в каком направлении вы хотите отправить почту ⬇️"

    await state.update_data(language=lang)
    await msg.answer(text, reply_markup=await choose_location_buttons(msg.text))


@dp.message_handler(Text(equals=[from_tashkent, from_samarkand]), state='location_mail')
async def mail_function_2(msg: types.Message, state: FSMContext):
    address = 'tashkent-samarkand' if msg.text == from_tashkent else 'samarkand-tashkent'
    await state.update_data(address=address)
    await state.set_state("phone_number")

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


async def process_phone_number(msg: types.Message, phone_number: str, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "uz")

    messages = {
        "uz": f"✅ Arizangiz qabul qilindi\n📲 Tez orada siz bilan bog'lanamiz!",
        "kr": f"✅ Аризангиз қабул қилинди\n📲 Тез орада сиз билан боғланамиз!",
        "ru": f"✅ Ваша заявка принята\n📲 Мы скоро с вами свяжемся!"
    }

    data = {
        "chat_id": str(msg.from_user.id),
        "full_name": msg.from_user.full_name,
        "delivery_address": user_data.get("address"),
        "offer_type": user_data.get("offer_type"),
        "phone_number": phone_number
    }
    requests.post(url="http://127.0.0.1:8000/api/offers/create/", data=data)

    await msg.answer(messages[lang], reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()

    offer_text = (
        f"📬 Yangi pochta jo'natilmoqda!\n\n"
        f"👤 Yuboruvchi: {msg.from_user.full_name}\n"
        f"📍 Yo‘nalish: {user_data.get('address')}\n"
        f"📞 Telefon: {phone_number}"
    )

    for group in groups:
        try:
            await bot.send_message(chat_id=group, text=offer_text)
        except Exception as e:
            print(f"Guruhga xabar yuborishda xatolik: {e}")


@dp.message_handler(state="phone_number", content_types=types.ContentType.CONTACT)
async def get_phone_number(msg: types.Message, state: FSMContext):
    await process_phone_number(msg, msg.contact.phone_number, state)
    await state.finish()


@dp.message_handler(state="phone_number", content_types=types.ContentType.TEXT)
async def get_phone_number_text(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+") and msg.text[1:].isdigit() and len(msg.text) == 13:
        await process_phone_number(msg, msg.text, state)
    else:
        user_data = await state.get_data()
        lang = user_data.get("language", "uz")

        error_messages = {
            "uz": "❌ Iltimos, to'g'ri telefon raqam kiriting yoki pastdagi tugmadan foydalaning.⬇️\n\nMisol: +998935365985",
            "kr": "❌ Илтимос, тўғри телефон рақам киритинг ёки пастдаги тугмадан фойдаланинг.⬇️\n\nМисол: +998935365985",
            "ru": "❌ Пожалуйста, введите правильный номер телефона или воспользуйтесь кнопкой ниже.⬇️\n\nПример: +998935365985"
        }

        await msg.answer(error_messages[lang])
