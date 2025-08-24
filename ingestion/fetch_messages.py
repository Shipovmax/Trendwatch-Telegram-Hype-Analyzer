# -*- coding: utf-8 -*-
"""Сбор сообщений из заданных каналов и сохранение в БД."""
import asyncio
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from config.settings import CHANNELS
from ingestion.telegram_client import get_client
from db.models import SessionLocal, Message

async def fetch_channel_messages(client, channel: str, limit: int = 300):
    """Асинхронно итерируем последние сообщения из канала."""
    try:
        entity = await client.get_entity(channel)
    except Exception as e:
        print(f"[WARN] Can't access {channel}: {e}")
        return

    async for msg in client.iter_messages(entity, limit=limit):
        if not msg.message:
            continue
        yield {
            "channel": channel,
            "message_id": msg.id,
            "text": msg.message,
            "views": msg.views or 0,
            "published_at": msg.date
        }

async def main():
    if not CHANNELS:
        print("CHANNELS пуст. Укажи список в .env (CHANNELS=chan1,chan2)")
        return

    client = get_client()
    await client.start()
    print(">> Telethon client started")

    db = SessionLocal()
    try:
        for ch in CHANNELS:
            print(f">> Fetching: {ch}")
            async for item in fetch_channel_messages(client, ch, limit=500):
                m = Message(
                    channel=item["channel"],
                    message_id=item["message_id"],
                    text=item["text"],
                    views=item["views"],
                    published_at=item["published_at"],
                    fetched_at=datetime.utcnow(),
                )
                try:
                    db.add(m)
                    db.commit()
                except IntegrityError:
                    # Дубликат пары (channel, message_id) — пропускаем
                    db.rollback()
        print(">> Done.")
    finally:
        db.close()
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

    