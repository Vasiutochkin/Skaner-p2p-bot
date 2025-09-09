from utils.logger import log
import time

def ranges_overlap(min_a, max_a, min_b, max_b):
    """Перевіряє чи перетинаються діапазони"""
    return not (max_a < min_b or max_b < min_a)

def calculate_spread(buy_price: float, sell_price: float) -> float:
    """Розрахунок спреду у відсотках"""
    if buy_price == 0:
        return 0.0
    return round(((sell_price - buy_price) / buy_price) * 100, 2)

def find_arbitrage(sell_order: dict, buy_order: dict, fiat: str, asset: str = "USDT"):
    """
    Шукає арбітражні можливості між SELL і BUY ордерами
    :param sell_order: ордер на продаж (dict)
    :param buy_order: ордер на купівлю (dict)
    :param fiat: фіатна валюта
    :param asset: актив (USDT, BTC)
    :return: dict або None
    """

    try:
        # методи оплати (перетин SELL і BUY)
        sell_payments = sell_order.get("payTypes", [])
        buy_payments = buy_order.get("payTypes", [])

        common_payments = list(set(sell_payments) & set(buy_payments))
        if not common_payments:
            return None


        # діапазони
        sell_min, sell_max = float(sell_order["minSingleTransAmount"]), float(sell_order["maxSingleTransAmount"])
        buy_min, buy_max = float(buy_order["minSingleTransAmount"]), float(buy_order["maxSingleTransAmount"])

        if not ranges_overlap(sell_min, sell_max, buy_min, buy_max):
            return None

        # ціни
        sell_price = float(sell_order["price"])  # він продає
        buy_price = float(buy_order["price"])    # він купує

        if buy_price >= sell_price:
            return None  # немає арбітражу

        spread = calculate_spread(buy_price, sell_price)

        # перетин діапазонів
        min_amount = max(sell_min, buy_min)
        max_amount = min(sell_max, buy_max)

        # прибуток
        profit_min = round((sell_price - buy_price) * min_amount, 2)
        profit_max = round((sell_price - buy_price) * max_amount, 2)

        result = {
            "fiat": fiat,
            "asset": asset,
            "sell_price": sell_price,
            "buy_price": buy_price,
            "spread": spread,
            "payment": ", ".join(common_payments),
            "min_amount": min_amount,
            "max_amount": max_amount,
            "profit_min": profit_min,
            "profit_max": profit_max,
            "seller": sell_order["nickName"],
            "buyer": buy_order["nickName"],
            "time": time.strftime("%H:%M"),

        }

        return result

    except Exception as e:
        log.error(f"Помилка у find_arbitrage({fiat}): {e}")
        return None
