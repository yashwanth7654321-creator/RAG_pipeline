# RAG Pipeline

This repository implements a Retrieval-Augmented Generation (RAG) pipeline for document-based question answering. It combines document ingestion, embedding-based retrieval, and LLM prompt generation, with optional Telegram bot support and MLflow experiment tracking.

## Key Features

- Ingests text and PDF documents from `knowledge_base/`
- Chunks documents and computes embeddings using `sentence-transformers`
- Stores embeddings in a local SQLite database (`rag.db`)
- Retrieves relevant context by cosine similarity
- Generates answers via `ollama` LLM model
- Provides a CLI query loop and optional Telegram bot interface
- Uses local semantic cache with `chromadb` to accelerate repeated queries
- Supports MLflow logging and evaluation when enabled

## Prerequisites

- Python 3.10+ (recommended)
- `ollama` installed and configured locally
- Telegram bot token if using the bot interface
- `mlflow` if you want experiment tracking

## Installation

1. Clone the repository
2. Create and activate a Python environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file at the repository root if using the Telegram bot:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

## Project Structure

- `main.py` - Root script for indexing documents, then running CLI query mode or MLflow tracking
- `bot_main.py` - Starts the Telegram bot with the configured token
- `config.py` - Central configuration values and builder helper
- `requirements.txt` - Python dependencies
- `knowledge_base/` - Document source folder for `.txt` and `.pdf` files
- `source_code/` - Core implementation modules:
  - `loader.py` - Loads text and PDF documents
  - `chunker.py` - Splits document text into chunks
  - `embedder.py` - Creates embeddings with SentenceTransformers
  - `database.py` - Manages SQLite embedding storage
  - `cache_DB.py` - Creates semantic cache collection with ChromaDB
  - `pipeline.py` - Indexing and query loop logic
  - `bot.py` - Telegram bot handlers and command routing
  - `llm.py` - Calls `ollama` to generate model responses
  - `create_prompt.py` - Builds the RAG prompt from context and history
  - `search_cache.py` - Looks up similar cached query responses
  - `store_cache.py` - Adds query/response pairs to cache
  - `msg_history.py` - Maintains short chat history
  - `ML_tracking_runner.py` - Runs queries with MLflow logging
  - `mlflow_logger.py` - MLflow helper wrappers
  - `evaluation.py` - Evaluates response faithfulness/relevance
  - `token_counter.py` - Token counting helper

## Usage

### 1. Index documents and use CLI mode

```bash
python main.py
```

This will:
- create `rag.db`
- index all documents in `knowledge_base/`
- enter a CLI loop for questions

### 2. Run the Telegram bot

```bash
python bot_main.py
```

Then message your bot or use `/ask <question>`.

### 3. Use experiment tracking

Set `RUN_EXPERIMENT = True` in `config.py` to run experiments from `main.py`.

### 4. Add documents

Place `.txt` or `.pdf` files inside `knowledge_base/`. The loader reads both file types automatically.

## Configuration

Important values in `config.py`:

- `EMBEDDING_MODEL` - SentenceTransformer embedding model
- `LLM_MODEL` - Ollama model name used for generation
- `TEXT_DATA_PATH` - Source document folder
- `DB_PATH` - SQLite database file path
- `CACHE_DB_PATH` - ChromaDB cache collection storage
- `TOP_K` - Number of retrieved chunks for prompt context
- `CHUNK_SIZE` / `CHUNK_OVERLAP` - Chunking parameters
- `USE_MLFLOW` - Enable logging with MLflow
- `RUN_EXPERIMENT` - Toggle grid-search experiment mode

## Notes

- `main.py` currently indexes documents and then runs a CLI query loop.
- `bot_main.py` starts the Telegram bot and uses the same embedding database and cache.
- Cached query results are stored in ChromaDB and reused when similarity is above `CACHE_THRESHOLD`.
- History is preserved per user and trimmed using `MAX_HISTORY` / `MAX_HISTORY_TOKENS`.

## Troubleshooting

- If `BOT_TOKEN` is missing, the bot will not start. Add it to `.env`.
- Make sure `ollama` is installed and the configured model is available.
- If embeddings are not found, rerun `python main.py` to rebuild `rag.db`.

## Recommended Next Steps

- Add a top-level `README.md` (this file)
- Add test coverage for retrieval and prompt generation
- Improve prompt formatting and response handling
- Persist chat history across restarts if needed
- Add better doc provenance display in answers
