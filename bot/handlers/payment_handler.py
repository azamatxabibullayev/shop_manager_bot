from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from bot.database import SessionLocal, Shop, Payment
from bot.config import PER_SQ_METER_PRICE, VAT_PERCENTAGE
import datetime

router = Router()


def calculate_payment(area: float) -> (float, float, float):
    # Calculate base payment and VAT
    base_payment = area * PER_SQ_METER_PRICE
    vat_amount = base_payment * VAT_PERCENTAGE / 100
    total = base_payment + vat_amount
    return base_payment, vat_amount, total


@router.message(F.text.casefold() == "payments")
async def list_payments(message: Message):
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
            callback_data=f"payment_{shop.id}"
        ))
    await message.answer("To'lovlar bo'limi: do'kon tanlang", reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("payment_"))
async def payment_details(callback: CallbackQuery):
    shop_id = int(callback.data.split("_")[1])
    session: Session = SessionLocal()
    shop = session.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        session.close()
        await callback.message.answer("Do'kon topilmadi!")
        return

    # Calculate payment for current month as an example.
    month = datetime.datetime.now().strftime("%Y-%m")
    base, vat, total = calculate_payment(shop.area)

    # Save the payment record (or update it) – here we add a new record for demonstration.
    payment = Payment(
        shop_id=shop.id,
        month=month,
        shop_area=shop.area,
        base_payment=base,
        vat_amount=vat,
        total_payment=total,
        left_over=total,  # assuming not paid yet
        paid=0
    )
    session.add(payment)
    session.commit()
    session.close()

    details = f"**{shop.name}** uchun {month} oyi to'lovi:\n" \
              f"Do'kon maydoni: {shop.area} kv.m\n" \
              f"Bir oylik asosiy to'lov: {base} so'm\n" \
              f"QQS ({VAT_PERCENTAGE}%): {vat} so'm\n" \
              f"Jami to'lov: {total} so'm"
    await callback.message.answer(details, parse_mode="Markdown")
