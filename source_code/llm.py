import ollama
from config import LLM_MODEL

def generate_response(prompt: str) -> str:
    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )
    return response['response']