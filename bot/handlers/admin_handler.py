from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.orm import Session
from bot.database import SessionLocal, Shop
from bot.utils import is_admin

router = Router()


@router.message(F.text.casefold() == "admin add shop")
async def admin_add_shop(message: Message):
    if not is_admin(message):
        await message.answer("Sizda admin huquqi yo'q!")
        return

    # For simplicity, we expect a message with shop details in a fixed format:
    # name;icon;area;registration_cert;payment_contract;cadastral_doc;lease_contract;photo
    try:
        data = message.get_args().split(";")
        if len(data) < 8:
            raise ValueError
        name, icon, area, reg_cert, pay_contract, cadastral, lease, photo = data
        area = float(area)
    except Exception as e:
        await message.answer("Xato format. Iltimos quyidagi formatda yuboring:\n"
                             "name;icon;area;registration_cert;payment_contract;cadastral_doc;lease_contract;photo")
        return

    session: Session = SessionLocal()
    shop = Shop(
        name=name.strip(),
        icon=icon.strip(),
        area=area,
        registration_cert=reg_cert.strip(),
        payment_contract=pay_contract.strip(),
        cadastral_doc=cadastral.strip(),
        lease_contract=lease.strip(),
        photo=photo.strip()
    )
    session.add(shop)
    session.commit()
    session.close()
    await message.answer(f"Do'kon '{name}' muvaffaqiyatli qo'shildi!")
