"""Настройки подключения к базе данных"""

import os

from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


SECRET_KEY = "python"

DATABASE_URI = f"postgresql://admin:admin@db:5432/best_parking_db"
TEST_DB_URI = "postgresql://test:test@db_test:5433/test_db"
