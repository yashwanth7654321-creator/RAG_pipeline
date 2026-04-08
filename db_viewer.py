from source_code.database import create_db, create_table, fetch_all_embeddings

def print_table(conn, cursor):
    cursor.execute("SELECT id, chunk, source, page FROM embeddings")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn , cursor = create_db()
view = print_table(conn, cursor)