import mlflow
from source_code.loader import load_documents
from source_code.chunker import chunk_text
from source_code.embedder import embed_text
from source_code.database import create_db, create_table, store_embeddings, text_normalizer
from source_code.pipeline import ask
from source_code.bot import run_bot
from source_code.cache_DB import create_cache_DB
from source_code.search_cache import search_cache
from source_code.msg_history import get_history
from source_code.mlflow_logger import start_experiment, log_params, log_metrics, log_artifacts, set_attributes
from source_code.evaluation import llm_evaluate
from source_code.token_counter import count_rag_tokens
from config import BOT_TOKEN, CHUNK_SIZE, LLM_MODEL, EMBEDDING_MODEL, TOP_K, USE_MLFLOW


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
    client, collection = create_cache_DB()
    #run_bot(BOT_TOKEN, conn, cursor, collection)
    
    
    while True:
        query = input("Ask a question: ")

        cached_response = search_cache(query, collection)

        if cached_response:
            print("\n Answer: ", cached_response)
        else:
            user_id = "local_user"
            response, retrived_chunks, retrival_time, generation_time = ask(query, conn, cursor, 
                                                                            user_id, collection)
            params = {
                    "embedding_model": EMBEDDING_MODEL,
                    "llm": LLM_MODEL,
                    "chunk_size": CHUNK_SIZE,
                    "top_k": TOP_K
                    }
            
            attributes = { 
                        "Dataset": "Indian_tourism",
                        "Version": "v1.0",
                        "Model": EMBEDDING_MODEL
                        }


            if USE_MLFLOW:
                run = start_experiment()
                log_params(params)
                set_attributes(attributes)
                scores = llm_evaluate(query, response, retrived_chunks)
                tokens_data = count_rag_tokens(query, retrived_chunks, response)
                metrics = {
                            "faithfulness": scores.get("faithfulness", 0),
                            "answer_relevance": scores.get("relevance", 0),
                            "retrieval_latency": retrival_time,
                            "generation_latency": generation_time,
                            "total_latency": retrival_time + generation_time,
                            "input_tokens": tokens_data["input_tokens"],
                            "output_tokens": tokens_data["output_tokens"],
                            "total_tokens": tokens_data["total_tokens"]
                }
                print("\nMetrics:\n", metrics)
                log_metrics(metrics)
                log_artifacts(query, retrived_chunks, response)
                mlflow.end_run()

            print("\n Answer: ", response)
            print("History:", get_history(user_id))

