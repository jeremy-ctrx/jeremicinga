"""Notification optionnelle (Telegram) des creneaux de blackout / signaux.

N'envoie jamais d'ordre, uniquement des messages informatifs. Ne fait rien
si TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID ne sont pas configures (.env).
"""

from __future__ import annotations

import os

import requests


def send_telegram_alert(message: str) -> bool:
    """Envoie un message Telegram si les variables d'environnement sont definies.

    Retourne False silencieusement si la notification n'est pas configuree
    (comportement attendu en Phase 1/2, ou tant que l'utilisateur n'a pas
    configure de bot).
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=10)
    return response.ok
