import requests

from config import settings


def send_telegram_message(chat_id, msg):
    params = {
        "text": msg,
        "chat_id": chat_id,
    }

    requests.get(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
