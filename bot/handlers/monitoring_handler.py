from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session
from bot.database import SessionLocal, Payment, ElectricityReading
import datetime

router = Router()


@router.message(F.text.casefold() == "monitoring")
async def monitoring_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Xizmat to'lovi", callback_data="monitor_service")],
        [InlineKeyboardButton(text="Elektr to'lovi", callback_data="monitor_electricity")],
        [InlineKeyboardButton(text="KPI hisobi", callback_data="monitor_kpi")]
    ])
    await message.answer("Monitoring bo'limi:", reply_markup=kb)


@router.callback_query(lambda c: c.data == "monitor_service")
async def monitor_service(callback):
    session: Session = SessionLocal()
    # Sample: total for current month, collected and pending shops
    month = datetime.datetime.now().strftime("%Y-%m")
    payments = session.query(Payment).filter(Payment.month == month).all()
    session.close()

    total_due = sum(p.total_payment for p in payments)
    total_paid = sum(p.paid for p in payments)
    pending_shops = [str(p.shop_id) for p in payments if p.paid < p.total_payment]

    text = f"**Xizmat to'lovi (oylik)**\n" \
           f"Jami to'lanishi lozim: {total_due}\n" \
           f"Hozirga qadar to'landi: {total_paid}\n" \
           f"Qolgan do'konlar: {', '.join(pending_shops) if pending_shops else 'yo\'q'}"
    await callback.message.answer(text, parse_mode="Markdown")


@router.callback_query(lambda c: c.data == "monitor_electricity")
async def monitor_electricity(callback):
    session: Session = SessionLocal()
    # Sample: electricity readings summary for current month
    month = datetime.datetime.now().strftime("%Y-%m")
    readings = session.query(ElectricityReading).all()  # refine query as needed
    session.close()

    total_usage = sum(r.usage for r in readings)
    text = f"**Elektr energiya to'lovi monitoringi**\n" \
           f"Jami ishlatilgan: {total_usage} kv"
    await callback.message.answer(text, parse_mode="Markdown")


@router.callback_query(lambda c: c.data == "monitor_kpi")
async def monitor_kpi(callback):
    # For demonstration, we simulate KPI calculation.
    kpi_percentage = 95  # In a real system, calculate based on payment/electricity submissions.
    text = f"**KPI hisobi**\n" \
           f"Xodimlar uchun umumiy KPI: {kpi_percentage}%"
    await callback.message.answer(text, parse_mode="Markdown")
