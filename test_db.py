# test_db.py
import os
from dotenv import load_dotenv

load_dotenv()

print("DATABASE_URL:", os.getenv("DATABASE_URL"))

try:
    import psycopg2
    print("psycopg2 installed")
except ImportError:
    print("psycopg2 NOT installed")

try:
    from sqlalchemy import create_engine
    print("sqlalchemy imported")
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        engine = create_engine(DATABASE_URL)
        print("Engine created successfully")
    else:
        print("DATABASE_URL is missing")
except Exception as e:
    print(f"Error: {e}")