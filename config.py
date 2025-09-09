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
    "EUR,USD,UAH,PLN,GBP,BRL,NGN,INR,RUB,CNY,KRW"
).split(",")

# 🪙 Який актив перевіряти (наприклад USDT, BTC, BUSD)
ASSET = os.getenv("ASSET", "USDT")

# 📈 Мінімальний спред (%) для сигналу
SPREAD_THRESHOLD = float(os.getenv("SPREAD_THRESHOLD", "3.0"))

# 🔄 Інтервал перевірки (секунди)
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3"))

# 💳 Методи оплати (повний список для вибраних валют)
ALLOWED_PAYMENTS = [
    # 🌍 Загальні міжнародні
    "BANK", "SWIFT", "SEPA", "SEPAinstant", "WIRE", "INTERNATIONAL_WIRE",
    "WISE", "REVOLUT", "N26", "ZEN", "PAYONEER", "PAYPAL", "PAYSERA",
    "STRIPE", "ADVCASH", "PERFECTMONEY",

    # 🇪🇺 Європа
    "ING", "Bunq", "Monese", "Klarna", "Skrill", "Neteller", "Vivid", "Fidor",

    # 🇺🇸 USD-зона
    "Chase", "BankofAmerica", "Citibank", "WellsFargo", "ACH", "Zelle",
    "CashApp", "Venmo",

    # 🇺🇦 Україна
    "MONOBANK", "PrivatBank", "PUMB", "A-Bank", "Oschadbank", "SenseSuperApp",
    "RaiffeisenBankAval", "Ukrgasbank", "OTPBank", "AlfaBankUA", "UniversalBank",

    # 🇵🇱 Польща
    "mBank", "PKOBP", "SantanderPL", "Millennium", "AliorBank", "INGPoland",

    # 🇬🇧 Британія
    "Barclays", "HSBC", "Lloyds", "NatWest", "Monzo", "Starling",

    # 🇧🇷 Бразилія
    "PIX", "BancoDoBrasil", "Bradesco", "Nubank", "SantanderBR", "Itaú",

    # 🇳🇬 Нігерія
    "GTBank", "AccessBank", "ZenithBank", "UBA", "FirstBank", "Opay", "PalmPay",

    # 🇮🇳 Індія
    "UPI", "IMPS", "PhonePe", "Paytm", "GooglePayIN", "SBI", "ICICI", "HDFC",

    # 🇷🇺 Росія
    "Sberbank", "Tinkoff", "RaiffeisenRU", "VTB", "AlfaBankRU", "QIWI", "YandexMoney",

    # 🇨🇳 Китай
    "Alipay", "WeChat", "BankOfChina", "ICBC", "CCB", "ABC", "UnionPay",

    # 🇰🇷 Корея
    "KakaoBank", "ShinhanBank", "KBKookmin", "NHBank", "WooriBank"
]
