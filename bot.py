import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
from config import BOT_TOKEN
from keyboards import main_menu_keyboard
from handlers.admin import admin_router
from handlers.shops import shop_router


async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Botga xush kelibsiz. Iltimos, quyidagi buyruqlardan birini tanlang:",
        reply_markup=main_menu_keyboard()
    )


async def main():
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.message.register(start_handler, Command("start"))
    dp.include_router(admin_router)
    dp.include_router(shop_router)

    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
