# app/services/db.py
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'hotel_db'),
}


@contextmanager
def get_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()