import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import InputFile

from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, back_main_menu_ru, back_main_menu_kr
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: types.Message):
    photo = InputFile("img.png")
    await message.reply_photo(
        photo=photo,
        caption=(
            """
📍 ИШОНЧЛИ ХАЛОЛ ТАКСИ ХИЗМАТИДАН ФОЙДАЛАНИНГ👇
            
@Toshkent_Samarqand_Taksi_Uz_Bot
@Toshkent_Samarqand_Taksi_Uz_Bot"""
        )
    )


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_kr]), state='*')
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_kr]), state='*')
async def back_main_menu_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=call.data, reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    data = {
        "chat_id": str(msg.from_user.id),
        "username": msg.from_user.username,
        "full_name": msg.from_user.full_name,
        "language": "uz"
    }

    response = requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/")
    if response.status_code == 404:
        requests.post(url="http://127.0.0.1:8000/api/telegram-users/create/", data=data)
    else:
        tg_user = response.json()
        requests.put(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    await state.set_state("location_mail")
    await state.set_state("location_taxi")
    await state.update_data(order_type='taxi')
    await msg.answer(text=f"""
👋 Assalomu alaykum {msg.from_user.first_name}! botimizga xush kelibsiz.

🛣 Qaysi yo'nalishda taksi buyurtma bermoqchisiz? ⬇️:""", reply_markup=await main_menu_buttons(msg.from_user.id))
    for admin in admins:
        await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {msg.from_user.full_name}""", parse_mode='HTML')
