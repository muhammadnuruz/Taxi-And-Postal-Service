import logging
import asyncio
from aiogram import executor

from bot.dispatcher import bot
from bot.handlers.schudele_handler import send_periodic_messages

admins = [1974800905, 725168806]
GROUP_IDS = [-1002609258755, -1002646296317, -1002407377689]
MESSAGE_TEXT = "📍 ИШОНЧЛИ ХАЛОЛ ТАКСИ ХИЗМАТИДАН ФОЙДАЛАНИНГ👇\n@Toshkent_Samarqand_Taksi_Uz_Bot"
BUTTON_TEXT = "📌 ИШОНЧЛИ ХАЛОЛ ТАКСИ ХИЗМАТИ"
BUTTON_URL = "https://t.me/Toshkent_Samarqand_Taksi_Uz_Bot"


async def on_startup(dp):
    asyncio.create_task(send_periodic_messages(bot, GROUP_IDS, MESSAGE_TEXT, BUTTON_TEXT, BUTTON_URL))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from aiogram import Dispatcher

    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
