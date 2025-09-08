import time
from bot.telegram_bot import TelegramBot
from exchanges.binance import fetch_binance
from utils.helpers import calculate_spread, get_flag, format_spread
from core.message_cache import is_new_offer, clear_cache, init_cache
from config import FIATS, ASSET, SPREAD_THRESHOLD, CHECK_INTERVAL
from utils.logger import log

active_messages = {}

def check_binance(bot: TelegramBot):
    for fiat in FIATS:
        buy_offers = fetch_binance("BUY", fiat, ASSET, limit=3)
        sell_offers = fetch_binance("SELL", fiat, ASSET, limit=3)

        if not buy_offers or not sell_offers:
            continue

        for buy in buy_offers:
            for sell in sell_offers:
                if sell["price"] <= buy["price"]:
                    continue

                common_methods = set(buy["methods"]) & set(sell["methods"])
                if not common_methods:
                    continue

                try:
                    buy_min, buy_max = float(buy["min_amount"]), float(buy["max_amount"])
                    sell_min, sell_max = float(sell["min_amount"]), float(sell["max_amount"])
                    real_min, real_max = max(buy_min, sell_min), min(buy_max, sell_max)
                    if real_min > real_max:
                        continue
                except (ValueError, TypeError):
                    continue

                spread = calculate_spread(buy["price"], sell["price"])
                if spread < SPREAD_THRESHOLD:
                    continue

                log.info(f"{fiat}: BUY={buy['price']} SELL={sell['price']} SPREAD={spread:.2f}%")

                key_buy = f"{fiat}:{buy['advNo']}:{buy['price']}"
                key_sell = f"{fiat}:{sell['advNo']}:{sell['price']}"

                if is_new_offer(key_buy) or is_new_offer(key_sell):
                    profit_min = (sell["price"] - buy["price"]) * real_min / buy["price"]
                    profit_max = (sell["price"] - buy["price"]) * real_max / buy["price"]

                    msg = (
                        f"🚀 <b>Арбітраж знайдено {get_flag(fiat)} ({fiat})!</b>\n\n"
                        f"🔴 SELL: {sell['price']} {sell['currency']} | {sell['seller_name']}\n"
                        f"🟢 BUY: {buy['price']} {buy['currency']} | {buy['seller_name']}\n\n"
                        f"📈 Спред: {format_spread(spread)}\n"
                        f"💳 Оплата: {', '.join(common_methods)}\n"
                        f"💵 Діапазон: {real_min:.2f} – {real_max:.2f} {fiat}\n"
                        f"💰 Прибуток: {profit_min:.2f} – {profit_max:.2f} {fiat}\n"
                        f"⏱ {time.strftime('%H:%M')}"
                    )

                    buttons = [[
                        {
                            "text": "SELL",
                            "url": f"https://p2p.binance.com/trade/sell/{sell['asset']}?fiat={fiat}&tradeType=SELL&advNo={sell['advId']}"
                        },
                        {
                            "text": "BUY",
                            "url": f"https://p2p.binance.com/trade/buy/{buy['asset']}?fiat={fiat}&tradeType=BUY&advNo={buy['advId']}"
                        }
                    ]]

                    sent = bot.send_message(msg, buttons)
                    if sent:
                        active_messages[key_buy] = sent["message_id"]
                        active_messages[key_sell] = sent["message_id"]

def main():
    clear_cache()
    init_cache()
    bot = TelegramBot()
    log.info("=== Skaner P2P Bot стартує ===")

    while True:
        try:
            check_binance(bot)
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            log.info("🛑 Бот зупинений користувачем")
            break
        except Exception as e:
            log.error(f"Помилка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
