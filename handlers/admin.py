from aiogram import types, Router
from aiogram.filters import Command
from config import ADMIN_ID
from keyboards import admin_menu_keyboard

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda ushbu funksiyaga kirish huquqi yo'q!")
        return
    await message.answer("Admin panelga hush kelibsiz!", reply_markup=admin_menu_keyboard())

@admin_router.message(lambda msg: msg.text == "Do'konlarni ro'yxatga olish")
async def register_shop(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ushbu funksiya faqat admin uchun!")
        return
    await message.answer("Yangi do'kon qo'shish uchun ma'lumotlani yuboring...")
