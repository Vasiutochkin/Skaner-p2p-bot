import asyncio
import aiohttp
from exchanges.binance import BinanceExchange

async def test_fetch_orders():
    ex = BinanceExchange()
    async with aiohttp.ClientSession() as session:
        data = await ex.fetch_orders(session, fiat="UAH", asset="USDT", limit=3)
        print("SELL ордери:")
        for s in data["SELL"]:
            print(s)
        print("\nBUY ордери:")
        for b in data["BUY"]:
            print(b)

if __name__ == "__main__":
    asyncio.run(test_fetch_orders())
