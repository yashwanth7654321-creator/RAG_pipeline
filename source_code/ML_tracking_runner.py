from config import LLM_MODEL, EMBEDDING_MODEL, USE_MLFLOW
from source_code.cache_DB import create_cache_DB
from source_code.mlflow_logger import start_experiment, log_params, log_metrics, log_artifacts, set_attributes
from source_code.evaluation import llm_evaluate
from source_code.token_counter import count_rag_tokens
from source_code.pipeline import ask
from source_code.search_cache import search_cache
from source_code.msg_history import get_history 
from config import USER_ID
import mlflow
def mlflow_tracking_run(query, config, conn, cursor, collection):
    
    cached_response = search_cache(query, collection)

    if cached_response:
        print("\n⚡ Cached:", cached_response)
        return

    params = {
        "embedding_model": EMBEDDING_MODEL,
        "llm": LLM_MODEL,
        **config
    }

    attributes = {
        "Dataset": "Indian_tourism",
        "Version": config["experiment_id"],
        "Models": f"{LLM_MODEL} + {EMBEDDING_MODEL}"
    }

    if USE_MLFLOW:
        run = start_experiment()
        log_params(params)
        set_attributes(attributes)

# If MLflow is disabled, we can run without logging the model

    response, chunks, rt, gt = ask(
        query, conn, cursor, USER_ID, collection, config
    )

    # Evaluate
    if USE_MLFLOW:

        scores = llm_evaluate(query, response, chunks)
        tokens = count_rag_tokens(query, chunks, response)

        metrics = {
            "faithfulness": scores.get("faithfulness", 0),
            "answer_relevance": scores.get("relevance", 0),
            "retrieval_latency": rt,
            "generation_latency": gt,
            "total_latency": rt + gt,
            "input_tokens": tokens["input_tokens"],
            "output_tokens": tokens["output_tokens"],
            "total_tokens": tokens["total_tokens"]
         }

    print("\nMetrics:\n", metrics)

    if USE_MLFLOW:
        log_metrics(metrics)
        log_artifacts(query, chunks, response)
        mlflow.end_run()

    print("\nAnswer:", response)
    print("History:", get_history(USER_ID))
