import asyncio
from aiogram import Dispatcher, Bot
from aiogram.bot import DefaultBotProperties
from bot.config import BOT_TOKEN
from bot.database import init_db

# Import routers
from bot.handlers import shop_handler, payment_handler, electricity_handler, monitoring_handler, admin_handler

async def main():
    # Initialize database
    init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default_bot_properties=DefaultBotProperties(parse_mode="Markdown")
    )
    dp = Dispatcher()

    # Register routers from each module
    dp.include_router(shop_handler.router)
    dp.include_router(payment_handler.router)
    dp.include_router(electricity_handler.router)
    dp.include_router(monitoring_handler.router)
    dp.include_router(admin_handler.router)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
