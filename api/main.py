# -*- coding: utf-8 -*-
"""Простой REST API на FastAPI: выдаёт топ трендов."""
from fastapi import FastAPI, Query
from typing import List, Dict
from analytics.trend_engine import compute_top_terms, compute_velocity

app = FastAPI(title="Trendwatch API", version="0.1.0")

@app.get("/trends/top")
def trends_top(hours: int = Query(1, ge=1, le=48), top_n: int = Query(10, ge=1, le=100)) -> List[Dict]:
    """Топ терминов за последние hours часов с оценкой velocity."""
    data = compute_top_terms(hours=hours, top_n=top_n)
    result = []
    for term, count in data:
        velocity = compute_velocity(term, hours=hours)
        result.append({"term": term, "count": count, "velocity": velocity})
    return result

    