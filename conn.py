import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_conn():
    try:
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )
        print("✅ Connected to the database.")
        return conn
    except Exception as e:
        print("❌ Failed to connect to the database:")
        print(e)
        return None