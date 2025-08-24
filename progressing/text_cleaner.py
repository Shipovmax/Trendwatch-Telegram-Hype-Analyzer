# -*- coding: utf-8 -*-
"""Примитивная очистка текста из Telegram."""
import re
import emoji

# Регулярки для ссылок/упоминаний/хэштегов
URL_RE = re.compile(r"https?://\S+|t\.me/\S+")
MENTION_RE = re.compile(r"@[\w_]+")          # @username
HASHTAG_RE = re.compile(r"#(\w+)")          # #tag -> сохраняем 'tag'

def clean_text(text: str) -> str:
    """Удаляем URL/упоминания, приводим к нижнему регистру, вычищаем пунктуацию."""
    if not text:
        return ""
    text = URL_RE.sub(" ", text)
    text = MENTION_RE.sub(" ", text)
    text = HASHTAG_RE.sub(r"\1", text)  # оставляем тело хэштега
    text = emoji.replace_emoji(text, replace=" ")  # эмодзи в пробелы
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)  # вся пунктуация -> пробел
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

    