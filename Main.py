from source_code.loader import load_documents
from source_code.chunker import chunk_text
from source_code.embedder import embed_text
from source_code.database import create_db, create_table, store_embeddings, text_normalizer
from source_code.pipeline import ask
from source_code.bot import run_bot
from source_code.cache_DB import create_cache_DB
from source_code.search_cache import search_cache
from source_code.msg_history import get_history
from config import BOT_TOKEN


def index_data(conn, cursor):
    docs =  load_documents()
    for doc in docs:
        text = doc["text"]
        source = doc["source"]
        page = doc["page"]
        chunks = chunk_text(text)

        for chunk in chunks:
            vector = embed_text(chunk)
            norm_chunk = text_normalizer(chunk)
            store_embeddings(conn, cursor, norm_chunk, vector, source, page)

if __name__ == "__main__":
    conn , cursor = create_db()
    create_table(conn, cursor)
    print("Indexing data...")
    index_data(conn, cursor)
    print("Data indexed successfully. You can now ask questions.")
    #run_bot(BOT_TOKEN, conn, cursor)
    client, collection = create_cache_DB()
    
    while True:
        query = input("Ask a question: ")
        cached_response = search_cache(query, client, collection)

        if cached_response:
            print("\n Answer: ", cached_response)
        else:
            user_id = 1
            response = ask(query, conn, cursor, user_id, collection)
            print("\n Answer: ", response)
            print("History for local_user:", get_history("local_user"))

