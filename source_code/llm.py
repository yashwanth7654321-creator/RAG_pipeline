import ollama
from config import LLM_MODEL
from config import MAX_OUTPUT_TOKENS, TEMPERATURE

def generate_response(prompt: str) -> str:
    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt,
        options = {"num_predict": MAX_OUTPUT_TOKENS,
                   "temperature": TEMPERATURE
                   }
    )
    return response['response']