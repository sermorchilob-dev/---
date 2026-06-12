import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Пытаемся получить URL из переменных окружения (сначала DATABASE_URL, потом NEXT_PUBLIC_API_URL)
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEXT_PUBLIC_API_URL")

if not DATABASE_URL:
    raise ValueError("❌ Нет переменной DATABASE_URL или NEXT_PUBLIC_API_URL в .env файле")

# Для Supabase заменяем префикс, если нужно (psycopg2)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

print("🔌 Подключение к БД:", DATABASE_URL.replace(os.getenv("PASSWORD", "****"), "****"))  # скрываем пароль

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована")
