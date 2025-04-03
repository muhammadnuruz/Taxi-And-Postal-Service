import logging
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot



async def send_periodic_messages(bot: Bot):
    GROUP_IDS = [-1002609258755, -1002646296317, -1002407377689]
    MESSAGE_TEXT = "📍 ИШОНЧЛИ ХАЛОЛ ТАКСИ ХИЗМАТИДАН ФОЙДАЛАНИНГ👇\n@Toshkent_Samarqand_Taksi_Uz_Bot"
    BUTTON_TEXT = "📌 ИШОНЧЛИ ХАЛОЛ ТАКСИ ХИЗМАТИ"
    BUTTON_URL = "https://t.me/Toshkent_Samarqand_Taksi_Uz_Bot"

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text=BUTTON_TEXT, url=BUTTON_URL))

    while True:
        for group_id in GROUP_IDS:
            try:
                await bot.send_message(chat_id=group_id, text=MESSAGE_TEXT, reply_markup=keyboard)
                logging.info(f"✅ Xabar {group_id} guruhga yuborildi.")
            except Exception as e:
                logging.error(f"❌ Xabar yuborishda xatolik ({group_id}): {e}")

        await asyncio.sleep(600)
