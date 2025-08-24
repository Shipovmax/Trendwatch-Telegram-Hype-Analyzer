# -*- coding: utf-8 -*-
"""Streamlit-дэшборд для просмотра трендов."""
import streamlit as st
import pandas as pd
from analytics.trend_engine import compute_top_terms, compute_velocity

st.set_page_config(page_title="Trendwatch Dashboard", layout="wide")
st.title("📈 Trendwatch — Telegram Hype Analyzer")

# Боковая панель с параметрами
hours = st.sidebar.select_slider("Период (часы)", options=[1, 6, 12, 24, 48], value=1)
top_n = st.sidebar.slider("Топ N", 5, 50, 10)

# Топ данных
top_data = compute_top_terms(hours=hours, top_n=top_n)
rows = []
for term, count in top_data:
    rows.append({"term": term, "count": count, "velocity": compute_velocity(term, hours=hours)})

df = pd.DataFrame(rows)
st.subheader("🔥 Топ трендов")
st.dataframe(df, use_container_width=True)

selected = st.selectbox("Выбери термин для деталей", [r["term"] for r in rows] if rows else [])
if selected:
    st.write(f"Текущие упоминания: **{int(df[df['term']==selected]['count'])}**")
    st.write(f"Скорость роста: **{float(df[df['term']==selected]['velocity'])}**")
    st.caption("MVP: детальная покадровая динамика появится позже (агрегации по часам)." )

    