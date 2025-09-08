import sqlite3
import os

DB_FILE = "messages_cache.db"

def init_cache():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def clear_cache():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_cache()

def is_new_offer(key: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM cache WHERE key = ?", (key,))
    exists = c.fetchone()
    if exists:
        conn.close()
        return False
    c.execute("INSERT INTO cache (key) VALUES (?)", (key,))
    conn.commit()
    conn.close()
    return True
