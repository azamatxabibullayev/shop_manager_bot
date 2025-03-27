from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from bot.database import SessionLocal, Shop

router = Router()


@router.message(F.text.casefold() == "shops")
async def list_shops(message: Message):
    session: Session = SessionLocal()
    shops = session.query(Shop).all()
    session.close()

    if not shops:
        await message.answer("Hozircha hech qanday do'kon qo'shilmagan.")
        return

    # Build inline keyboard with shops
    kb = InlineKeyboardMarkup()
    for shop in shops:
        kb.add(InlineKeyboardButton(
            text=f"{shop.icon or ''} {shop.name}",
            callback_data=f"shop_{shop.id}"
        ))
    await message.answer("Do'konlar ro'yxati:", reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("shop_"))
async def shop_details(callback: CallbackQuery):
    shop_id = int(callback.data.split("_")[1])
    session: Session = SessionLocal()
    shop = session.query(Shop).filter(Shop.id == shop_id).first()
    session.close()

    if not shop:
        await callback.message.answer("Do'kon topilmadi!")
        return

    # Prepare details text (you can add PDF links if stored as files/URLs)
    details = f"**{shop.name}**\n" \
              f"ID: {shop.id}\n" \
              f"Maydon: {shop.area} kv.m\n" \
              f"Ro'yxatdan o'tish guvohnomasi: {shop.registration_cert}\n" \
              f"To'lov shartnomasi: {shop.payment_contract}\n" \
              f"Kadastr hujjati: {shop.cadastral_doc}\n" \
              f"Ijara shartnomasi: {shop.lease_contract}\n" \
              f"Foto: {shop.photo}"
    await callback.message.answer(details, parse_mode="Markdown")
