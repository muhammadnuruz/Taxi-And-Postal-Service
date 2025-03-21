from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import uz_language, ru_language, kr_language


async def language_buttons():
    design = [
        [InlineKeyboardButton(text=uz_language, callback_data='language_uz'),
         InlineKeyboardButton(text=kr_language, callback_data='language_kr'),
         InlineKeyboardButton(text=ru_language, callback_data='language_ru')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
