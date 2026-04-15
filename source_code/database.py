import sqlite3
import numpy as np
from config import CHUNK_OVERLAP, CHUNK_SIZE, EXPERIMENT_ID

def create_db():
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    conn.commit()
    return conn, cursor

def create_table(conn,cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk TEXT,
        chunk_size INTEGER,
        overlap INTEGER,
        source TEXT,
        page INTEGER,
        vector BLOB,
        experiment_id TEXT,
        UNIQUE (chunk, chunk_size, overlap, source, page))""")
    conn.commit()
    return ("Table is created")

def text_normalizer(text):
    return " ".join(text.strip().split())

def store_embeddings(conn, cursor, chunk, vector, source, page, config):

    chunk_size = config["chunk_size"]
    overlap = config["overlap"]
    experiment_id = config["experiment_id"]

    cursor.execute("INSERT OR IGNORE INTO embeddings (chunk, vector, source, page, chunk_size, overlap, experiment_id) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (chunk, vector.tobytes(), source, page, chunk_size, overlap, experiment_id))
    conn.commit()
    return ("entry inserted (or ignored if duplicate)")

def fetch_all_embeddings(conn, cursor, chunk_size, overlap):
    
    cursor.execute("SELECT chunk, vector FROM embeddings WHERE chunk_size=? AND overlap=?", (chunk_size, overlap))
    result = []

    for chunk, vector in cursor.fetchall():
        vector = np.frombuffer(vector, dtype=np.float32)
        result.append((chunk, vector))
        conn.commit()
    return result







                           