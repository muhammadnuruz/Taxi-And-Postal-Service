import json

import requests
from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, choice_language, choice_language_ru, \
    back_main_menu_ru, be_driver_ru, be_driver, be_driver_kr, choice_language_kr, taxi_text, mail_text, taxi_text_kr, \
    mail_text_kr, taxi_text_ru, mail_text_ru, back_main_menu_kr, from_tashkent, from_samarkand


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [taxi_text, mail_text],
            [be_driver, choice_language]
        ]
    elif tg_user['language'] == 'kr':
        design = [
            [taxi_text_kr, mail_text_kr],
            [be_driver_kr, choice_language_kr]
        ]
    else:
        design = [
            [taxi_text_ru, mail_text_ru],
            [be_driver_ru, choice_language_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [[back_main_menu]]
    else:
        design = [[back_main_menu_ru]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def choose_location_buttons(text: str):
    design = [
        [from_tashkent, from_samarkand],
    ]
    if text == mail_text:
        design.append([back_main_menu])
    elif text == mail_text_kr:
        design.append([back_main_menu_kr])
    else:
        design.append([back_main_menu_ru])
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
