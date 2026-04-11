import ollama
from config import LLM_MODEL

def llm_evaluate(query, response, chunks):
    context = "\n".join([chunk for chunk in chunks])

    prompt = f"""
    You are an evaluator for a RAG system.

    Question: {query}

    Context:
    {context}

    Answer:
    {response}

    Score the following from 0 to 1:
    1. Faithfulness (Is answer grounded in context?)
    2. Answer Relevance (Does it answer the question?)

    Return ONLY in this format:
    faithfulness: <score>
    relevance: <score>
    """
    result = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    text = result["message"]["content"]

    scores = {}
    for line in text.split("\n"):
        if "faithfulness" in line.lower():
            scores["faithfulness"] = float(line.split(":")[1].strip())
        elif "relevance" in line.lower():
            scores["relevance"] = float(line.split(":")[1].strip())
    return scores

# {
#   "model": "llama2",
#   "created_at": "2026-04-10T13:20:00Z",
#   "message": {
#     "role": "assistant",
#     "content": "faithfulness: 0.9\nrelevance: 0.8"
#   },
#   "done": True
# }
#op will be
#
# {
#   "faithfulness": 0.9,
#   "relevance": 0.8
# }