import mlflow
from source_code.pipeline import ask
from source_code.evaluation import llm_evaluate
from source_code.token_counter import count_rag_tokens
from source_code.database import create_db
from source_code.cache_DB import create_cache_DB
from config import EMBEDDING_MODEL, EXPERIMENT_ID, LLM_MODEL, build_config

user_id = "test_user"

test_queries = [
    "which place is famous for Lord shiva",
    "who introduced christianity in india",
    "where i can do adventures tourism in india"
]

chunk_sizes = [200, 500]
top_ks = [3, 5]
overlap = build_config()["overlap"]
def run_experiment(chunk_size, top_k, conn, cursor, client, collection, overlap):

    mlflow.set_experiment("RAG_Grid_Search")

    with mlflow.start_run():

        mlflow.log_params({
            "chunk_size": chunk_size,
            "top_k": top_k,
            "embedding_model": EMBEDDING_MODEL,
            "llm": LLM_MODEL,
            "overlap": overlap
        })

        mlflow.set_tags({
            "Dataset": "Indian_tourism",
            "Experiment_id": f"chunk{chunk_size}_topk{top_k}_overlap{overlap}",
            "Models": f"{LLM_MODEL} + {EMBEDDING_MODEL}"})


        all_faithfulness = []
        all_relevance = []
        all_latency = []
        all_tokens = []       

        for query in test_queries:

            current_config = build_config(chunk_size=chunk_size, top_k=top_k, overlap=overlap)

            response, chunks, rt, gt = ask(
                query, conn, cursor, user_id, collection,
                current_config
            )  

            scores = llm_evaluate(query, response, chunks)
            tokens = count_rag_tokens(query, chunks, response)

            all_faithfulness.append(scores.get("faithfulness", 0))
            all_relevance.append(scores.get("relevance", 0))
            all_latency.append(rt + gt)
            all_tokens.append(tokens["total_tokens"])

        metrics = {
            "avg_faithfulness": sum(all_faithfulness) / len(all_faithfulness),
            "avg_relevance": sum(all_relevance) / len(all_relevance),
            "avg_latency": sum(all_latency) / len(all_latency),
            "avg_tokens": sum(all_tokens) / len(all_tokens)
        }

        mlflow.log_metrics(metrics)

        print(f"Done: chunk={chunk_size}, top_k={top_k} → {metrics}")

def run_experiments():
    """Run grid search experiments"""
    conn, cursor = create_db()
    client, collection = create_cache_DB()
    
    for chunk_size in chunk_sizes:
        for top_k in top_ks:
            run_experiment(chunk_size, top_k, conn, cursor, client, collection, overlap)