# -*- coding: utf-8 -*-
"""Выделение терминов (простая токенизация + стоп-слова)."""
from typing import List, Set
import re
from pathlib import Path

STOPWORDS: Set[str] = set()

def load_stopwords(path: str = "data/stopwords.txt") -> None:
    """Загружаем стоп-слова из файла один раз."""
    global STOPWORDS
    p = Path(path)
    if p.exists():
        STOPWORDS = {w.strip() for w in p.read_text(encoding="utf-8").splitlines() if w.strip()}
    else:
        STOPWORDS = set()

def extract_terms(text: str) -> List[str]:
    """Возвращаем слова длиной 3+ без стоп-слов."""
    if not STOPWORDS:
        load_stopwords()
    tokens = re.findall(r"\b[\w\d]{3,}\b", text.lower())
    return [t for t in tokens if t not in STOPWORDS]

    