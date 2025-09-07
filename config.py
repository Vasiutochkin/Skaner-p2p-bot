import os
from dotenv import load_dotenv

# завантажуємо .env файл
load_dotenv()

# 🔑 Дані для Bybit
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# 🔑 Дані для Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 💱 Основні торгові параметри
FIAT = os.getenv("FIAT", "EUR")
ASSET = os.getenv("ASSET", "USDT")

# 📈 Поріг спреду
SPREAD_THRESHOLD = float(os.getenv("SPREAD_THRESHOLD", "1.0"))

# 🔄 Інтервал перевірки
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))

# 💳 Методи оплати
ALLOWED_PAYMENTS = [
    "BANK",
    "BBVABank",
    "Bunq",
    "ING",
    "N26",
    "Paysera",
    "SEPA",
    "SEPAinstant",
    "ZEN",
]
