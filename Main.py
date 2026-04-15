from source_code.loader import load_documents
from source_code.chunker import chunk_text
from source_code.embedder import embed_text
from source_code.database import create_db, create_table, store_embeddings, text_normalizer
from source_code.cache_DB import create_cache_DB
from config import build_config, RUN_EXPERIMENT
from source_code.ML_tracking_runner import mlflow_tracking_run
from source_code.experiment_logger import run_experiments

def index_data(conn, cursor, config):
    docs =  load_documents()
    for doc in docs:
        text = doc["text"]
        source = doc["source"]
        page = doc["page"]
        chunks = chunk_text(text, config)

        for chunk in chunks:
            vector = embed_text(chunk)
            norm_chunk = text_normalizer(chunk)
            store_embeddings(conn, cursor, norm_chunk, vector, source, page, config)

if __name__ == "__main__":
    conn , cursor = create_db()
    create_table(conn, cursor)
    config = build_config()
    print("Indexing data...")
    index_data(conn, cursor, config)
    print("Data indexed successfully. You can now ask questions.")
    client, collection = create_cache_DB()
    #run_bot(BOT_TOKEN, conn, cursor, collection)
    if RUN_EXPERIMENT:
        print("Running Grid Search Experiments...")
        run_experiments()

    else:
        print("Running CLI Mode...")
        while True:
            query = input("\nAsk a question: ")
            config = build_config()
            mlflow_tracking_run(query, config, conn, cursor, collection)