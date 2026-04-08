import sqlite3
import numpy as np

def create_db():
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    conn.commit()
    return conn, cursor

def create_table(conn,cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk TEXT UNIQUE,
        source TEXT,
        page INTEGER,
        vector BLOB)""")
    conn.commit()
    return ("Table is created")

def text_normalizer(text):
    return " ".join(text.strip().split())

def store_embeddings(conn, cursor, chunk, vector, source, page):  #Needs a list of vectors
    cursor.execute("INSERT OR IGNORE INTO embeddings (chunk, vector, source, page) VALUES (?, ?, ?, ?)", 
                   (chunk, vector.tobytes(), source, page))
    conn.commit()
    return ("entry inserted (or ignored if duplicate)")

def fetch_all_embeddings(conn, cursor):
    cursor.execute("SELECT chunk, vector FROM embeddings")
    result = []

    for chunk, vector in cursor.fetchall():
        vector = np.frombuffer(vector, dtype=np.float32)
        result.append((chunk, vector))
        conn.commit()
    return result







                           