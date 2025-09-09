from bot.telegram_bot import TelegramBot
from core.strategy import find_arbitrage

def test_full_arbitrage():
    sell_order = {
        "price": "42.7",
        "minSingleTransAmount": "1000",
        "maxSingleTransAmount": "2000",
        "payTypes": ["PrivatBank"],
        "nickName": "User-SELL"
    }
    buy_order = {
        "price": "41.5",
        "minSingleTransAmount": "500",
        "maxSingleTransAmount": "3000",
        "payTypes": ["PrivatBank"],
        "nickName": "User-BUY"
    }

    result = find_arbitrage(sell_order, buy_order, fiat="UAH", asset="USDT")
    print("Arbitrage result:", result)

    if result:
        bot = TelegramBot()
        resp = bot.send_arbitrage(result)
        print("Telegram response:", resp)

if __name__ == "__main__":
    test_full_arbitrage()
