import requests
from config import ALLOWED_PAYMENTS

BINANCE_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def fetch_binance(trade_type="BUY", fiat="EUR", asset="USDT", limit=3):
    payload = {
        "page": 1,
        "rows": limit * 5,
        "payTypes": [],
        "asset": asset,
        "tradeType": trade_type,
        "fiat": fiat,
        "publisherType": None,
    }

    try:
        resp = session.post(BINANCE_URL, json=payload, timeout=5).json()
        data = resp.get("data", [])
        if not data:
            return []

        offers = []
        for offer in data:
            adv = offer.get("adv", {})
            advertiser = offer.get("advertiser", {})
            if not adv or not advertiser:
                continue

            adv_no = adv.get("advNo")
            price = adv.get("price")
            min_amount = adv.get("minSingleTransAmount")
            max_amount = adv.get("maxSingleTransAmount")
            trade_methods = adv.get("tradeMethods", [])
            seller_name = advertiser.get("nickName", "Невідомо")

            if not adv_no or not price or not trade_methods:
                continue

            try:
                price = float(price)
            except ValueError:
                continue

            methods = [m.get("identifier") for m in trade_methods if m.get("identifier")]

            if not any(m in ALLOWED_PAYMENTS for m in methods):
                continue

            offers.append(
                {
                    "exchange": "binance",
                    "side": trade_type.lower(),
                    "price": price,
                    "currency": fiat,
                    "asset": asset,
                    "advNo": adv_no,
                    "methods": methods,
                    "min_amount": min_amount,
                    "max_amount": max_amount,
                    "seller_name": seller_name,  # 👈 додаємо ім’я продавця
                }
            )

            if len(offers) >= limit:
                break

        return offers

    except requests.exceptions.Timeout:
        print("[WARN] Binance API timeout")
        return []
    except Exception as e:
        print("[ERROR] Binance fetch error:", e)
        return []
