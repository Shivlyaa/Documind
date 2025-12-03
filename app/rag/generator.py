# app/rag/generator.py

from app.routes.chat import get_llm
import re

model = get_llm()

def strip_think(text: str) -> str:
    """
    This removes any reasoning traces like:
    <think> ... </think>
    """
    # Remove any <think>...</think> block (DOTALL = span multiple lines)
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned.strip()

def get_response(prompt: str) -> str:
    """
    Returns a clean, final string answer from the LLM.
    """
    raw = model.invoke(prompt)   # raw HF output (string)
    final = strip_think(raw)     # remove reasoning block
    return final

