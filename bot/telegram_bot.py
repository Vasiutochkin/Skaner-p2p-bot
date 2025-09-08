import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import log

class TelegramBot:
    def __init__(self, token: str = TELEGRAM_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id

    def send_message(self, text: str, buttons: list[list[dict]] | None = None):
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if buttons:
            payload["reply_markup"] = {"inline_keyboard": buttons}

        r = requests.post(f"{self.api_url}/sendMessage", json=payload, timeout=5)
        data = r.json()
        if not data.get("ok"):
            log.error(f"[Telegram] Error: {data}")
        return data.get("result", {})

    def delete_message(self, message_id: int):
        payload = {"chat_id": self.chat_id, "message_id": message_id}
        r = requests.post(f"{self.api_url}/deleteMessage", json=payload, timeout=5)
        return r.json()
