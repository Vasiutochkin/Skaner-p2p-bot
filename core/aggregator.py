from core.strategy import find_arbitrage
from utils.logger import log

async def find_opportunities(exchanges, session, fiat: str, asset: str = "USDT", limit: int = 5):
    """
    Повний перебір: беремо топ-N SELL і BUY по всіх біржах, шукаємо арбітраж
    """
    all_sells, all_buys = [], []

    for ex in exchanges:
        try:
            orders = await ex.fetch_orders(session, fiat, asset, limit=limit)
            all_sells.extend(orders.get("SELL", []))
            all_buys.extend(orders.get("BUY", []))
        except Exception as e:
            log.error(f"[{ex.__class__.__name__}] Помилка fetch_orders: {e}")

    total_combinations = len(all_sells) * len(all_buys)
    results = []

    for sell in all_sells:
        for buy in all_buys:
            result = find_arbitrage(sell, buy, fiat, asset)
            if result and result["spread"] >= 3:
                results.append(result)

    log.info(f"[{fiat}] перевірено {total_combinations} комбінацій, знайдено {len(results)} арбітражів")
    return results
