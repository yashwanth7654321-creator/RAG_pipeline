USE_MLFLOW = True
RUN_EXPERIMENT = False

USER_ID = "Test_user"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DB_PATH = "rag.db"
CACHE_DB_PATH = "semantic_cache.db"
TEXT_DATA_PATH = "knowledge_base"
TOP_K = 6
CHUNK_SIZE = 200
#CHUNK_OVERLAP = int(CHUNK_SIZE * 0.2)
CHUNK_OVERLAP = 40
LLM_MODEL = "mistral"
TEMPERATURE = 0.7
MAX_HISTORY = 3
MAX_HISTORY_TOKENS = 200
MAX_CACHE_SIZE = 5
CACHE_THRESHOLD = 0.8
MAX_OUTPUT_TOKENS = 500
EXPERIMENT_ID = f"chunk{CHUNK_SIZE}_topk{TOP_K}_overlap{CHUNK_OVERLAP}"


def build_config(chunk_size=None, overlap=None, top_k=None, experiment_id="default"):
    return {
        "chunk_size": chunk_size or CHUNK_SIZE,
        "overlap": overlap or CHUNK_OVERLAP,
        "top_k": top_k or TOP_K,
        "experiment_id": experiment_id or EXPERIMENT_ID
    }
