import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import log

API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(text: str, buttons: list[list[dict]] | None = None):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    log.debug(f"[Telegram] Sending payload: {payload}")

    r = requests.post(f"{API_URL}/sendMessage", json=payload)
    data = r.json()
    log.debug(f"[Telegram] Response: {data}")

    return data.get("result", {})


def delete_message(message_id: int):
    payload = {"chat_id": TELEGRAM_CHAT_ID, "message_id": message_id}
    r = requests.post(f"{API_URL}/deleteMessage", json=payload)
    data = r.json()
    log.debug(f"[Telegram] Delete response: {data}")
    return data
