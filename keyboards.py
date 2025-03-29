from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Do'konlar bo'limi")],
            [KeyboardButton(text="Savdo kompleks to'lovlari")],
            [KeyboardButton(text="Elektr energiya hisoblari")],
            [KeyboardButton(text="Monitoring")]
        ],
        resize_keyboard=True
    )
    return kb


def admin_menu_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Do'konlarni ro'yhatga olish")],
            [KeyboardButton(text="Statistika")]
        ],
        resize_keyboard=True
    )
    return kb


def shops_inline_keyboard(shops: list):
    kb = InlineKeyboardMarkup(row_width=3)
    for shop in shops:
        kb.insert(InlineKeyboardButton(text=f"{shop['shop_number']}", callback_data=f"shop_{shop['id']}"))
    return kb
