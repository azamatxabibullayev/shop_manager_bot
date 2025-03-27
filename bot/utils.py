from aiogram.types import Message
from bot.config import ADMIN_IDS

def is_admin(message: Message) -> bool:
    return message.from_user.id in ADMIN_IDS
