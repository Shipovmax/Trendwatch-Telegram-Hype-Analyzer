# **Область проекта (MVP)**
    
 • Источник данных: Telegram (через Telethon)
 • Сбор сообщений из выбранных публичных каналов
 • Хранение данных в PostgreSQL (или SQLite для теста)
 • Обработка текста: очистка, токенизация, лемматизация, удаление стоп-слов
 • Метрики:
 • количество упоминаний слов/хэштегов
 • скорость роста (velocity)
 • новизна (появление впервые за N часов)
 • Аналитика: топ трендов за последние N часов/дней
 • Интерфейсы:
 • Streamlit-дэшборд (топ трендов + графики)
 • Telegram-бот (уведомления о новых трендах)


# **Архитектура (MVP)**

[Telegram Channels]  
      │  
      ▼  
 [Telethon Adapter] → [Preprocessing] → [PostgreSQL]  
      │  
      ▼  
 [Analytics Core] → [Trend Score Engine]  
      │  
      ├──> [Streamlit Dashboard]  
      └──> [Telegram Bot Alerts]  


# **Схема БД**

messages
 • id (PK)
 • channel (text)
 • message_id (int)
 • text (text)
 • views (int)
 • reactions (jsonb/null)
 • published_at (timestamp)
 • fetched_at (timestamp)

terms
 • id (PK)
 • term (text, unique)
 • lang (varchar)

message_terms
 • message_id (FK → messages)
 • term_id (FK → terms)
 • weight (float)

trend_stats
 • id (PK)
 • term_id (FK → terms)
 • window_start (timestamp)
 • window_end (timestamp)
 • count (int)
 • velocity (float)
 • novelty (float)
 • trend_score (float, индекс)


# **Алгоритм Trend Score**

Для слова/хэштега t:
 • count = число упоминаний за последнее окно (например, 1 час)
 • velocity = разница с предыдущим окном
 • novelty = 1, если слово новое за последние N часов, иначе < 1
 • trend_score = 0.6 * normalized(count) + 0.3 * normalized(velocity) + 0.1 * novelty


# **Интерфейсы**

1. Streamlit Dashboard
 • Фильтр по периоду: 1h / 6h / 24h
 • Таблица: топ-10 трендов (слово, score, count, velocity, пример сообщений)
 • График: динамика упоминаний выбранного тренда

2. Telegram Bot
 • Команда /top → присылает топ-5 трендов
 • Алерт при trend_score > 0.7 и росте velocity:

    //🚀 Новый тренд: "Мобилизация"
    //Упоминаний за час: 128
    //Рост: +400% по сравнению с прошлым часом


# **Этичность и ToS**

 • Используются только публичные данные из Telegram
 • Соблюдаются лимиты API
 • Персональные данные не сохраняются
 • Логи содержат только техническую информацию


