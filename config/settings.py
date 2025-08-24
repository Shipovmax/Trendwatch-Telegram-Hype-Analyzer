# -*- coding: utf-8 -*-
"""Telegram-бот на aiogram для выдачи топа трендов."""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import BOT_TOKEN, TOP_N
from analytics.trend_engine import compute_top_terms, compute_velocity

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🔥 Trendwatch Bot запущен. Команда /top покажет тренды.")

@dp.message(Command("top"))
async def top_cmd(message: types.Message):
    data = compute_top_terms(hours=1, top_n=TOP_N)
    if not data:
        await message.answer("Пока нет данных. Сперва запусти парсер: `python ingestion/fetch_messages.py`.")
        return
    lines = ["🔥 Топ трендов за 1 час:"]
    for i, (term, count) in enumerate(data, start=1):
        vel = compute_velocity(term, hours=1)
        lines.append(f"{i}. {term} — {count} упомин., velocity={vel:+}")
    await message.answer("\n".join(lines))

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN пуст. Укажи токен в .env")
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main()

    