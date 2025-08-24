# -*- coding: utf-8 -*-
"""Фабрика Telethon-клиента."""
from telethon import TelegramClient
from config.settings import API_ID, API_HASH, SESSION_NAME

def get_client() -> TelegramClient:
    """Создаёт и возвращает TelegramClient. Требует API_ID/API_HASH в .env."""
    if not API_ID or not API_HASH:
        raise RuntimeError("API_ID/API_HASH не заданы. Заполни .env")
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    return client

    