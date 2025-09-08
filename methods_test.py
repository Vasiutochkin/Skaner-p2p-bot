import requests

BINANCE_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def check_currency(fiat="EUR", asset="USDT"):
    payload = {
        "page": 1,
        "rows": 1,
        "payTypes": [],
        "asset": asset,
        "tradeType": "BUY",
        "fiat": fiat
    }
    resp = requests.post(BINANCE_URL, json=payload).json()
    data = resp.get("data", [])
    print(f"{fiat}: {'✅ дані є' if data else '❌ немає даних'}")

for fiat in ["EUR", "USD", "UAH", "PLN", "GBP", "NGN", "BRL", "INR", "RUB", "CNY", "KRW"]:
    check_currency(fiat)
