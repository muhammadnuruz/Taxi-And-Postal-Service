from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, mail_text, from_tashkent, \
    from_samarkand


async def main_menu_buttons(chat_id: int):
    design = [
        [from_tashkent, from_samarkand],
        [mail_text]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    design = [[back_main_menu]]
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
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
