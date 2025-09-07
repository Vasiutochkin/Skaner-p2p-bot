import requests
from config import ALLOWED_PAYMENTS
from utils.logger import log

BYBIT_URL = "https://www.bybit.com/x-api/fiat/otc/item/online"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
session.headers.update(HEADERS)

# 📌 Маппінг кодів платіжних методів → зрозумілі назви
PAYMENT_METHODS = {
    "65": "SEPA",
    "416": "Revolut",
    "14": "Wise",
    "150": "Bank Transfer",
    "118": "N26",
    "51": "ING",
    "78": "Paysera",
    "328": "BBVABank",
    "330": "Bunq",
    "303": "ZEN",
    # ❗ якщо зустрінемо нові коди — треба буде доповнити
}


def fetch_bybit(trade_type="BUY", fiat="EUR", asset="USDT", limit=3):
    """
    Отримати P2P оффери з Bybit у такому ж форматі, як з Binance.
    :param trade_type: "BUY" або "SELL"
    :param fiat: Напр. "EUR"
    :param asset: Напр. "USDT"
    :param limit: кількість результатів
    :return: список офферів
    """

    # Bybit: side = "0" → BUY (купити USDT), "1" → SELL (продати USDT)
    side = "0" if trade_type.upper() == "BUY" else "1"

    payload = {
        "userId": "",
        "tokenId": asset,
        "currencyId": fiat,
        "payment": [],
        "side": side,
        "size": str(limit * 5),  # беремо більше і потім фільтруємо
        "page": "1",
        "amount": "",
        "orderType": "",
        "canTrade": False,
        "shield": 0,
        "sortType": "OVERALL_RANKING"
    }

    try:
        resp = session.post(BYBIT_URL, json=payload, timeout=10).json()

        if resp.get("ret_code") != 0:
            log.error(f"[Bybit] API error: {resp.get('ret_msg')}")
            return []

        items = resp["result"].get("items", [])
        offers = []

        for item in items:
            try:
                price = float(item.get("price", 0))
                adv_id = str(item.get("id"))
                seller_name = item.get("nickName", "Невідомо")
                min_amount = item.get("minAmount")
                max_amount = item.get("maxAmount")

                # конвертуємо payment IDs у зрозумілі назви
                payments_raw = item.get("payments", [])
                payments = [PAYMENT_METHODS.get(str(p), str(p)) for p in payments_raw]

                # фільтр по способам оплати
                if not any(m in ALLOWED_PAYMENTS for m in payments):
                    continue

                offers.append(
                    {
                        "exchange": "bybit",
                        "side": trade_type.lower(),
                        "price": price,
                        "currency": fiat,
                        "asset": asset,
                        "advNo": adv_id,
                        "methods": payments,
                        "min_amount": min_amount,
                        "max_amount": max_amount,
                        "seller_name": seller_name,
                    }
                )

                if len(offers) >= limit:
                    break
            except Exception as e:
                log.warning(f"[Bybit] Skip bad item: {e}")
                continue

        log.info(f"[Bybit] Знайдено {len(offers)} офферів ({trade_type} {asset}/{fiat})")
        return offers

    except requests.exceptions.Timeout:
        log.warning("[Bybit] API timeout")
        return []
    except Exception as e:
        log.error(f"[Bybit] fetch error: {e}")
        return []


if __name__ == "__main__":
    print("=== Тест Bybit P2P API ===")

    buy_offers = fetch_bybit("BUY", "EUR", "USDT", limit=3)
    print("\nBUY OFFERS:")
    for o in buy_offers:
        print(o)

    sell_offers = fetch_bybit("SELL", "EUR", "USDT", limit=3)
    print("\nSELL OFFERS:")
    for o in sell_offers:
        print(o)
