from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from bot.database import SessionLocal, ElectricityReading, Shop
import datetime

router = Router()


@router.message(F.text.casefold() == "electricity")
async def list_electricity_shops(message: Message):
    session: Session = SessionLocal()
    shops = session.query(Shop).all()
    session.close()

    if not shops:
        await message.answer("Hozircha hech qanday do'kon qo'shilmagan.")
        return

    kb = InlineKeyboardMarkup()
    for shop in shops:
        kb.add(InlineKeyboardButton(
            text=f"{shop.name}",
            callback_data=f"elec_{shop.id}"
        ))
    await message.answer("Elektr energiya hisoblari uchun do'kon tanlang", reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("elec_"))
async def electricity_details(callback: CallbackQuery):
    shop_id = int(callback.data.split("_")[1])
    session: Session = SessionLocal()
    shop = session.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        session.close()
        await callback.message.answer("Do'kon topilmadi!")
        return

    # For demonstration, we simulate readings.
    previous = 1234
    current = 1300
    usage = current - previous
    tariff = 1100
    calculated = usage * tariff
    paid = 100000  # demo value
    debt = calculated - paid if paid < calculated else 0
    overpaid = paid - calculated if paid > calculated else 0

    # Save the reading record
    reading = ElectricityReading(
        shop_id=shop.id,
        previous=previous,
        current=current,
        usage=usage,
        tariff=tariff,
        calculated_amount=calculated,
        paid_amount=paid,
        debt=debt,
        overpaid=overpaid
    )
    session.add(reading)
    session.commit()
    session.close()

    details = f"**Elektr energiya hisoblari**\n" \
              f"Do'kon: {shop.name}\n" \
              f"Oldingi ko'rsatkich: {previous}\n" \
              f"Joriy ko'rsatkich: {current}\n" \
              f"Ishlatilgan: {usage} kv\n" \
              f"Tarif: {tariff} so'm\n" \
              f"Hisoblandi: {calculated} so'm\n" \
              f"To'landi: {paid} so'm\n" \
              f"Qarz: {debt} so'm\n" \
              f"Ortiqcha: {overpaid} so'm"
    await callback.message.answer(details, parse_mode="Markdown")
