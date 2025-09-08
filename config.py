import os
from dotenv import load_dotenv

# завантажуємо .env файл
load_dotenv()

# 🔑 Дані для Bybit (якщо використовуєш)
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# 🔑 Дані для Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 💱 Список валют для моніторингу (робочі валюти)
FIATS = os.getenv(
    "FIATS",
    "EUR,USD,UAH,PLN,GBP,INR,CNY"
).split(",")

# 🪙 Який актив перевіряти (наприклад USDT, BTC, BUSD)
ASSET = os.getenv("ASSET", "USDT")

# 📈 Мінімальний спред (%) для сигналу
SPREAD_THRESHOLD = float(os.getenv("SPREAD_THRESHOLD", "1.0"))

# 🔄 Інтервал перевірки (секунди) → робимо швидший
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3"))

# 💳 Методи оплати (інформаційно)
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
    "WISE",
    "REVOLUT",
    "MONOBANK",
    "PrivatBank",
    "PUMB",
    "A-Bank",
    "Oschadbank",
    "SenseSuperApp",
    "RaiffeisenBankAval",
]
