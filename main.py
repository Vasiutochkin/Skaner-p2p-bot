import time
from bot.telegram_bot import send_message, delete_message
from exchanges.binance import fetch_binance
from utils.helpers import calculate_spread
from core.message_cache import is_new_offer, clear_cache
from config import FIAT, ASSET, SPREAD_THRESHOLD, CHECK_INTERVAL
from utils.logger import log

active_messages = {}  # {key: message_id} де key = advNo:price


def format_spread(spread: float) -> str:
    """Форматує спред з кольоровими емодзі"""
    if spread >= SPREAD_THRESHOLD * 3:
        return f"🟢 <b>{spread:.2f}%</b>"
    elif spread >= SPREAD_THRESHOLD * 2:
        return f"🟡 <b>{spread:.2f}%</b>"
    else:
        return f"🔴 <b>{spread:.2f}%</b>"


def orders_overlap(buy, sell) -> bool:
    """Перевіряє чи перетинаються ордери по сумах"""
    try:
        buy_min, buy_max = float(buy["min_amount"]), float(buy["max_amount"])
        sell_min, sell_max = float(sell["min_amount"]), float(sell["max_amount"])
        return not (sell_min > buy_max or buy_min > sell_max)
    except (ValueError, TypeError):
        return False


def check_binance():
    """Основна перевірка арбітражу на Binance"""
    buy_offers = fetch_binance("BUY", FIAT, ASSET, limit=3)
    sell_offers = fetch_binance("SELL", FIAT, ASSET, limit=3)

    if not buy_offers or not sell_offers:
        log.warning("Немає даних від Binance")
        return

    for buy in buy_offers:
        for sell in sell_offers:
            # Ціна має бути адекватна
            if sell["price"] <= buy["price"]:
                continue

            # Спільні методи оплати
            common_methods = set(buy["methods"]) & set(sell["methods"])
            if not common_methods:
                continue

            # Перевірка по сумах
            if not orders_overlap(buy, sell):
                continue

            # Рахуємо спред
            spread = calculate_spread(buy["price"], sell["price"])
            log.info(
                f"Binance: BUY={buy['price']} SELL={sell['price']} "
                f"SPREAD={spread:.2f}% METHODS={', '.join(common_methods)}"
            )

            if spread >= SPREAD_THRESHOLD:
                key_buy = f"{buy['advNo']}:{buy['price']}"
                key_sell = f"{sell['advNo']}:{sell['price']}"

                msg = (
                    f"🔄 <b>Арбітраж знайдено!</b>\n"
                    f"🔴 Binance | Продавець: <b>{sell['seller_name']}</b>\n"
                    f"   Ціна: {sell['price']} {sell['currency']}\n"
                    f"   Мін: {sell['min_amount']} {sell['currency']}, "
                    f"Макс: {sell['max_amount']} {sell['currency']}\n"
                    f"──────────\n"
                    f"🟢 Binance | Продавець: <b>{buy['seller_name']}</b>\n"
                    f"   Ціна: {buy['price']} {buy['currency']}\n"
                    f"   Мін: {buy['min_amount']} {buy['currency']}, "
                    f"Макс: {buy['max_amount']} {buy['currency']}\n"
                    f"──────────\n"
                    f"📈 Спред: {format_spread(spread)}\n"
                    f"💳 Метод: <b>{', '.join(common_methods)}</b>\n"
                )

                # Кнопки з посиланням на ордери Binance
                buttons = [[
                    {
                        "text": "Відкрити ордер (SELL)",
                        "url": f"https://p2p.binance.com/advertiserDetail?advertiserNo={sell['advNo']}"
                    },
                    {
                        "text": "Відкрити ордер (BUY)",
                        "url": f"https://p2p.binance.com/advertiserDetail?advertiserNo={buy['advNo']}"
                    }
                ]]

                # Відправляємо тільки якщо це новий оффер
                if is_new_offer(key_buy) or is_new_offer(key_sell):
                    log.info("Відправляємо повідомлення в Telegram")
                    sent = send_message(msg, buttons=buttons)
                    if sent:
                        active_messages[key_buy] = sent["message_id"]
                        active_messages[key_sell] = sent["message_id"]

    # 🔄 Видаляємо неактуальні повідомлення
    for key, msg_id in list(active_messages.items()):
        still_alive = any(
            f"{o['advNo']}:{o['price']}" == key for o in (buy_offers + sell_offers)
        )
        if not still_alive:
            log.info(f"Ордер {key} більше недоступний → видаляємо повідомлення")
            delete_message(msg_id)
            del active_messages[key]


def main():
    clear_cache()
    log.info("=== Skaner P2P Bot (Binance) стартує ===")

    try:
        while True:
            check_binance()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        log.info("🛑 Бот зупинено користувачем")
    except Exception as e:
        log.error(f"Помилка у циклі: {e}")


if __name__ == "__main__":
    main()
