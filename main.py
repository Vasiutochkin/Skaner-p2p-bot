import asyncio
import aiohttp

from exchanges.binance import BinanceExchange
from bot.telegram_bot import TelegramBot, MIN_SPREAD
from core.aggregator import find_opportunities
from core.message_cache import MessageCache
from utils.logger import log

FIATS = ["UAH", "EUR", "USD", "PLN", "GBP"]

async def main_loop():
    bot = TelegramBot()
    cache = MessageCache(ttl=300)
    exchanges = [BinanceExchange()]

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                for fiat in FIATS:
                    results = await find_opportunities(exchanges, session, fiat, asset="USDT", limit=5)

                    for result in results:
                        if result["spread"] < MIN_SPREAD:
                            continue

                        cache_key = f"{result['fiat']}-{result['seller']}-{result['buyer']}-{result['payment']}"
                        if not cache.get(cache_key):
                            bot.send_arbitrage(result)
                            cache.set(cache_key, True)
                            log.info(f"Відправлено арбітраж: {result}")

            except Exception as e:
                log.error(f"Помилка в циклі: {e}")

            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main_loop())
