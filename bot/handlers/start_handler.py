import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ContentType

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, back_main_menu_ru, choice_language_kr
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]), state='*')
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu, back_main_menu_ru]), state='*')
async def back_main_menu_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=call.data, reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Тилни танланг

-------------

Выберите язык""", reply_markup=await language_buttons())
    except KeyError:
        if tg_user.get('language') == 'uz':
            await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        elif tg_user.get('language') == 'kr':
            await msg.answer(text=f"Бот янгиланди ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    for admin in admins:
        await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={call.from_user.id}'>{call.from_user.id}</a>
Username: @{call.from_user.username}
Ism-Familiya: {call.from_user.full_name}""", parse_mode='HTML')
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        'language': call.data.split('_')[-1]
    }
    requests.post(url=f"http://127.0.0.1:8000/api/telegram-users/create/", data=data)
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text=f"""
👋 Assalomu alaykum {call.from_user.first_name}! botimizga xush kelibsiz.

✅Quyidagi xizmatlardan birini tanlang:""",
                                  reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == "kr":
        await call.message.answer(text=f"""
👋 Ассалому алайкум {call.from_user.first_name}! ботимизга хуш келибсиз.

✅Қуйидаги хизматлардан бирини танланг:""", reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text=f"""
👋 Привет {call.from_user.first_name}! Добро пожаловать в наш бот.

✅Выберите одну из следующих услуг:""", reply_markup=await main_menu_buttons(call.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru, choice_language_kr]))
async def change_language_function_1(msg: types.Message):
    await msg.answer(text="""
Tilni tanlang

-------------

Тилни танланг

-------------

Выберите язык""", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.put(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'kr':
        await call.message.answer(text="Тил ўзгартирилди 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))


def get_drivers_list():
    response = requests.get("http://127.0.0.1:8000/api/drivers/")
    if response.status_code == 200:
        drivers_data = response.json()['results']
        return [driver['chat_id'] for driver in drivers_data]
    else:
        return []


@dp.message_handler(content_types=ContentType.PHOTO)
async def delete_photo_if_not_driver(message: types.Message):
    drivers_chat_ids = get_drivers_list()

    if message.from_user.id not in drivers_chat_ids:
        await message.delete()
