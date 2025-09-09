import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import log

MIN_SPREAD = 3

class TelegramBot:
    def __init__(self, token: str = TELEGRAM_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id

    def send_message(self, text: str, buttons: list[list[dict]] | None = None):
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"}
        if buttons:
            payload["reply_markup"] = {"inline_keyboard": buttons}

        r = requests.post(f"{self.api_url}/sendMessage", json=payload, timeout=5)
        data = r.json()
        if not data.get("ok"):
            log.error(f"[Telegram] Error: {data}")
        return data.get("result", {})

    def send_arbitrage(self, result: dict):
        fiat = result["fiat"]
        asset = result["asset"]
        spread = result["spread"]
        spread_emoji = "🟢" if spread > 5 else "🟡" if spread > 0 else "🔴"

        text = (
            f"🚀 Арбітраж знайдено {fiat} ({asset})!\n\n"
            f"🔴 SELL: {result['sell_price']} {fiat} | {result['seller']}\n"
            f"🟢 BUY: {result['buy_price']} {fiat} | {result['buyer']}\n\n"
            f"📉 Спред: {spread_emoji} {spread}%\n"
            f"💳 Оплата: {result['payment']}\n"
            f"💵 Діапазон: {result['min_amount']} – {result['max_amount']} {fiat}\n"
            f"💰 Прибуток: {result['profit_min']} – {result['profit_max']} {fiat}\n"
            f"⏰ {result['time']}"
        )

        buttons = [
            [{"text": "SELL", "callback_data": "sell"}],
            [{"text": "BUY", "callback_data": "buy"}]
        ]

        return self.send_message(text, buttons)
