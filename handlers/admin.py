from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from keyboards import admin_menu_keyboard
from database import get_connection

admin_router = Router()


@admin_router.message(Command("start"))
async def start_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin panelga hush kelibsiz!", reply_markup=admin_menu_keyboard())
    else:
        await message.answer("Assalomu alaykum! Siz admin emassiz. Iltimos, tegishli bo'limlardan foydalaning.")


@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda ushbu funksiyaga kirish huquqi yo'q!")
        return
    await message.answer("Admin panelga hush kelibsiz!", reply_markup=admin_menu_keyboard())


class ShopRegistration(StatesGroup):
    shop_number = State()
    name = State()
    details = State()
    registration_certificate = State()
    contract_pdf = State()
    cadastre_pdf = State()
    lease_contract_pdf = State()
    photo = State()
    area = State()


@admin_router.message(lambda msg: msg.text == "Do'konlarni ro'yhatga olish")
async def begin_shop_registration(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ushbu funksiya faqat admin uchun!")
        return
    await message.answer("Iltimos, do'kon raqamini kiriting:")
    await state.set_state(ShopRegistration.shop_number)


@admin_router.message(ShopRegistration.shop_number)
async def process_shop_number(message: types.Message, state: FSMContext):
    try:
        shop_number = int(message.text)
    except ValueError:
        await message.answer("Raqam kiritishda xatolik. Iltimos, to'g'ri raqam kiriting:")
        return
    await state.update_data(shop_number=shop_number)
    await message.answer("Do'kon nomini kiriting:")
    await state.set_state(ShopRegistration.name)


@admin_router.message(ShopRegistration.name)
async def process_shop_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Do'kon haqida qisqacha ma'lumot kiriting:")
    await state.set_state(ShopRegistration.details)


@admin_router.message(ShopRegistration.details)
async def process_shop_details(message: types.Message, state: FSMContext):
    await state.update_data(details=message.text)
    await message.answer("Ro'yxatdan o'tish guvohnomasi (PDF) fayl manzilini kiriting:")
    await state.set_state(ShopRegistration.registration_certificate)


@admin_router.message(ShopRegistration.registration_certificate)
async def process_registration_certificate(message: types.Message, state: FSMContext):
    await state.update_data(registration_certificate=message.text)
    await message.answer("Shartnoma (PDF) fayl manzilini kiriting:")
    await state.set_state(ShopRegistration.contract_pdf)


@admin_router.message(ShopRegistration.contract_pdf)
async def process_contract_pdf(message: types.Message, state: FSMContext):
    await state.update_data(contract_pdf=message.text)
    await message.answer("Kadastr hujjati (PDF) fayl manzilini kiriting:")
    await state.set_state(ShopRegistration.cadastre_pdf)


@admin_router.message(ShopRegistration.cadastre_pdf)
async def process_cadastre_pdf(message: types.Message, state: FSMContext):
    await state.update_data(cadastre_pdf=message.text)
    await message.answer("Ijara shartnomasi (PDF) fayl manzilini kiriting:")
    await state.set_state(ShopRegistration.lease_contract_pdf)


@admin_router.message(ShopRegistration.lease_contract_pdf)
async def process_lease_contract_pdf(message: types.Message, state: FSMContext):
    await state.update_data(lease_contract_pdf=message.text)
    await message.answer("3x4 foto manzili (URL yoki fayl manzili) kiriting:")
    await state.set_state(ShopRegistration.photo)


@admin_router.message(ShopRegistration.photo)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await message.answer("Do'kon maydonini (kvadrat metr) kiriting:")
    await state.set_state(ShopRegistration.area)


@admin_router.message(ShopRegistration.area)
async def process_area(message: types.Message, state: FSMContext):
    try:
        area = float(message.text)
    except ValueError:
        await message.answer("Iltimos, to'g'ri raqam kiriting:")
        return
    await state.update_data(area=area)

    data = await state.get_data()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO shops (shop_number, name, details, registration_certificate, contract_pdf, cadastre_pdf, lease_contract_pdf, photo, area)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["shop_number"],
            data["name"],
            data["details"],
            data["registration_certificate"],
            data["contract_pdf"],
            data["cadastre_pdf"],
            data["lease_contract_pdf"],
            data["photo"],
            data["area"]
        ))
        conn.commit()
        await message.answer("Do'kon muvaffaqiyatli qo'shildi!")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    finally:
        conn.close()
    await state.clear()


class TariffUpdate(StatesGroup):
    month = State()
    rate = State()


@admin_router.message(lambda msg: msg.text == "Tariflarni o'zgartirish")
async def begin_tariff_update(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ushbu funksiya faqat admin uchun!")
        return
    await message.answer("Qaysi oy uchun tarifni yangilamoqchisiz? (masalan: 2025-01)")
    await state.set_state(TariffUpdate.month)


@admin_router.message(TariffUpdate.month)
async def process_tariff_month(message: types.Message, state: FSMContext):
    await state.update_data(month=message.text)
    await message.answer("Yangi tarif (kvadrat metr uchun summa) kiriting:")
    await state.set_state(TariffUpdate.rate)


@admin_router.message(TariffUpdate.rate)
async def process_tariff_rate(message: types.Message, state: FSMContext):
    try:
        rate = float(message.text)
    except ValueError:
        await message.answer("Iltimos, to'g'ri raqam kiriting:")
        return
    data = await state.get_data()
    month = data["month"]
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM service_payments WHERE month = ? LIMIT 1", (month,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE service_payments SET rate = ? WHERE id = ?", (rate, existing["id"]))
        else:
            cursor.execute("SELECT id, area FROM shops")
            shops = cursor.fetchall()
            for shop in shops:
                calculated_amount = shop["area"] * rate
                cursor.execute("""
                    INSERT INTO service_payments (shop_id, month, area, rate, calculated_amount, previous_balance, paid_amount, due_amount, tax_amount)
                    VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?)
                """, (
                    shop["id"], month, shop["area"], rate, calculated_amount, calculated_amount,
                    calculated_amount * 0.12))
        conn.commit()
        await message.answer("Tarif muvaffaqiyatli yangilandi!")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    finally:
        conn.close()
    await state.clear()


@admin_router.message(lambda msg: msg.text == "Statistika")
async def show_statistics(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ushbu funksiya faqat admin uchun!")
        return
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(calculated_amount) as total_calculated FROM service_payments")
        service_total = cursor.fetchone()["total_calculated"] or 0

        cursor.execute("SELECT SUM(calculated_amount) as total_electric FROM electricity_readings")
        electric_total = cursor.fetchone()["total_electric"] or 0

        cursor.execute("SELECT COUNT(*) as unpaid_count FROM monitoring WHERE unpaid_shops != ''")
        unpaid_count = cursor.fetchone()["unpaid_count"] or 0

        text = (
            f"**Statistika hisobotlari**\n\n"
            f"Xizmat to'lovlari bo'yicha umumiy miqdor: {service_total}\n"
            f"Elektr energiya hisoblari bo'yicha umumiy miqdor: {electric_total}\n"
            f"To'lanmagan monitoring holatlar soni: {unpaid_count}"
        )
        await message.answer(text)
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    finally:
        conn.close()
