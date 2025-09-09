import aiohttp

BINANCE_P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

class BinanceExchange:
    def __init__(self):
        self.name = "Binance"

    async def fetch_orders(self, session, fiat: str, asset: str = "USDT", limit: int = 5):
        """
        Отримати SELL і BUY ордери з Binance P2P
        """
        results = {"SELL": [], "BUY": []}

        for trade_type in ["SELL", "BUY"]:
            payload = {
                "page": 1,
                "rows": limit,
                "payTypes": [],
                "asset": asset,
                "tradeType": trade_type,
                "fiat": fiat
            }

            async with session.post(BINANCE_P2P_URL, json=payload) as resp:
                data = await resp.json()
                adverts = data.get("data", [])
                for adv_data in adverts:
                    adv = adv_data["adv"]
                    advertiser = adv_data["advertiser"]
                    results[trade_type].append({
                        "price": adv["price"],
                        "minSingleTransAmount": adv["minSingleTransAmount"],
                        "maxSingleTransAmount": adv["maxSingleTransAmount"],
                        "payTypes": [
                            m.get("tradeMethodShortName")
                            for m in adv.get("tradeMethods", [])
                            if m.get("tradeMethodShortName")
                        ],
                        "nickName": advertiser.get("nickName", "Unknown"),
                        "exchange": self.name
                    })

        return results
