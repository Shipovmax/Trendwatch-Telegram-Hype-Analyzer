# -*- coding: utf-8 -*-
"""Наивные метрики трендов: топ терминов и скорость роста."""
from datetime import datetime, timedelta
from collections import Counter
from typing import List, Tuple

from db.models import SessionLocal, Message
from processing.text_cleaner import clean_text
from processing.term_extractor import extract_terms

def compute_top_terms(hours: int = 1, top_n: int = 10) -> List[Tuple[str, int]]:
    """Считает топ слов за последние N часов (простая частота)."""
    since = datetime.utcnow() - timedelta(hours=hours)
    db = SessionLocal()
    try:
        q = db.query(Message).filter(Message.published_at >= since)
        counter = Counter()
        for m in q.yield_per(500):
            text = clean_text(m.text or "")
            terms = extract_terms(text)
            counter.update(terms)
        return counter.most_common(top_n)
    finally:
        db.close()

def term_count(term: str, since: datetime, until: datetime) -> int:
    """Сколько раз встречается термин в интервале [since, until)."""
    db = SessionLocal()
    try:
        q = db.query(Message).filter(Message.published_at >= since, Message.published_at < until)
        cnt = 0
        for m in q.yield_per(500):
            text = clean_text(m.text or "")
            terms = extract_terms(text)
            cnt += sum(1 for t in terms if t == term)
        return cnt
    finally:
        db.close()

def compute_velocity(term: str, hours: int = 1) -> float:
    """Скорость роста: разница между текущим и предыдущим окном по часам."""
    now = datetime.utcnow()
    cur_since = now - timedelta(hours=hours)
    prev_since = now - timedelta(hours=2*hours)
    cur = term_count(term, cur_since, now)
    prev = term_count(term, prev_since, cur_since)
    return float(cur - prev)

    