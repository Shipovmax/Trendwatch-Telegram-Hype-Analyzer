# -*- coding: utf-8 -*-
"""Создание таблиц в базе."""
from db.models import Base, engine

def init_db():
    print(">> Creating tables...")
    Base.metadata.create_all(bind=engine)
    print(">> Done.")

if __name__ == "__main__":
    init_db()

    