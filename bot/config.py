import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "123456789").split(",")]

# Tariff configuration for payment calculation
PER_SQ_METER_PRICE = 13000  # in sum per sq.m.
VAT_PERCENTAGE = 12  # for service payment
