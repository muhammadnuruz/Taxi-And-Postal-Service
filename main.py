import logging
import asyncio
from aiogram import executor
from bot.dispatcher import bot, dp
from bot.handlers.schudele_handler import send_periodic_messages

admins = [1974800905, 725168806]

async def on_startup(dp):
    asyncio.create_task(send_periodic_messages(bot))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
