# 🚀 Trendwatch — Telegram Hype Analyzer

<p align="center">
  <b>Open-source система для анализа трендов в Telegram</b><br>
  Отслеживай хайп, находи новые темы, смотри аналитику в реальном времени 📈
</p>


---

## ✨ Возможности
- 📥 Сбор сообщений из публичных **Telegram-каналов** (через Telethon)
- 🗄 Хранение данных в **PostgreSQL**
- 🧹 Очистка текста (эмодзи, ссылки, стоп-слова)
- 🔎 Выделение ключевых слов и хэштегов
- 📊 Метрики трендов:
  - `count` — количество упоминаний
  - `velocity` — скорость роста
  - `novelty` — новые слова за период
- 📺 Красивый **Streamlit Dashboard**
- 🤖 **Telegram-бот** для алертов и команды `/top`

---

## 🛠 Архитектура
```mermaid
flowchart TD
    A[Telegram Channels] --> B[Telethon Adapter]
    B --> C[Preprocessing]
    C --> D[(PostgreSQL)]
    D --> E[Analytics Engine]
    E --> F[Streamlit Dashboard]
    E --> G[Telegram Bot Alerts]
```

---

## 📂 Структура проекта
```bash
trendwatch/
├── README.md                # описание проекта
├── .env.example             # переменные окружения
├── docker-compose.yml       # запуск Postgres
├── requirements.txt         # зависимости Python
├── config/
│   └── settings.py          # конфигурация
├── data/
│   └── stopwords.txt        # стоп-слова
├── ingestion/
│   ├── telegram_client.py   # клиент Telethon
│   └── fetch_messages.py    # сбор сообщений
├── processing/
│   ├── text_cleaner.py      # очистка текста
│   └── term_extractor.py    # выделение слов/хэштегов
├── analytics/
│   ├── trend_engine.py      # расчёт трендов
│   └── scheduler.py         # запуск задач
├── api/
│   └── main.py              # FastAPI (REST API)
├── dashboard/
│   └── app.py               # Streamlit-дэшборд
├── bot/
│   └── bot.py               # Telegram-бот
└── db/
    ├── models.py            # SQLAlchemy модели
    └── migrations/          # alembic миграции
```

---


## 📺 Интерфейсы

### 🖥 Streamlit Dashboard
- 🔎 Фильтр по периоду: `1h` / `6h` / `24h`
- 📋 Таблица: топ-10 трендов (слово, score, count, velocity)
- 📈 График динамики популярности

### 🤖 Telegram Bot
- `/top` → топ-5 трендов прямо в чате
- ⚡ Уведомления при резком всплеске

---

## ⚖️ Этичность
- Используются только **публичные данные Telegram**
- Соблюдаются лимиты API
- Персональные данные не сохраняются

---

<p align="center">
  💡 Разрабатывается как pet-project. Любой может <b>форкнуть</b> и доработать 🚀
</p>