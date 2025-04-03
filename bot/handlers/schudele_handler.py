import asyncio
import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_periodic_messages(bot: Bot, group_ids: list, message_text: str, button_text: str, button_url: str, interval: int = 600):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=button_text, url=button_url))

    while True:
        for group_id in group_ids:
            try:
                await bot.send_message(chat_id=group_id, text=message_text, reply_markup=keyboard)
                logging.info(f"✅ Xabar {group_id} guruhga yuborildi.")
            except Exception as e:
                logging.error(f"❌ Xabar yuborishda xatolik ({group_id}): {e}")

        await asyncio.sleep(interval)
