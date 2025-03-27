from aiogram import types, Router
from keyboards import shops_inline_keyboard
from database import get_connection

shop_router = Router()

@shop_router.message(lambda message: message.text == "Do'konlar bo'limi")
async def list_shops(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, shop_number, name FROM shops")
    shops = cursor.fetchall()
    conn.close()
    if shops:
        shops_list = [{"id": row["id"], "shop_number": row["shop_number"], "name": row["name"]} for row in shops]
        kb = shops_inline_keyboard(shops_list)
        await message.answer("Do'konlar ro'yxati:", reply_markup=kb)
    else:
        await message.answer("Hali do'konlar qo'shilmagan.")

@shop_router.callback_query(lambda c: c.data and c.data.startswith("shop_"))
async def shop_details(callback: types.CallbackQuery):
    shop_id = callback.data.split("_")[1]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shops WHERE id = ?", (shop_id,))
    shop = cursor.fetchone()
    conn.close()
    if shop:
        text = (f"Do'kon: {shop['name']}\n"
                f"Raqam: {shop['shop_number']}\n"
                f"Ma'lumot: {shop['details']}\n"
                f"Hajmi: {shop['area']} кв.м")
        await callback.message.answer(text)
    else:
        await callback.message.answer("Do'kon topilmadi.")
