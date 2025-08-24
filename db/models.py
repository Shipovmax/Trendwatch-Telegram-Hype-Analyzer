# -*- coding: utf-8 -*-
"""SQLAlchemy-модели и подключение к базе."""
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from config.settings import DATABASE_URL

Base = declarative_base()

class Message(Base):
    """Таблица сообщений из Telegram (минимально необходимая)."""
    __tablename__ = "messages"
    __table_args__ = (
        UniqueConstraint("channel", "message_id", name="uq_channel_message"),
    )

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(255), index=True)        # username канала
    message_id = Column(BigInteger, index=True)      # ID сообщения в канале
    text = Column(Text)                              # текст сообщения
    views = Column(Integer, default=0)               # просмотры (если есть)
    published_at = Column(DateTime, index=True)      # время публикации
    fetched_at = Column(DateTime, default=datetime.utcnow, index=True)  # когда мы забрали

# Подключение к БД и фабрика сессий
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

