import json
import os
from typing import List, Dict

# Store chat history inside storage/memory (better organization)
MEMORY_DIR = "storage/memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

# How many past turns you want to keep
MAX_TURNS = 6   # 3 Q/A exchanges


def get_memory_path(document_id: str) -> str:
    """Return the file path for a document's chat memory."""
    return os.path.join(MEMORY_DIR, f"{document_id}.json")


def load_memory(document_id: str) -> List[Dict]:
    """Load chat memory from local JSON file."""
    path = get_memory_path(document_id)

    if not os.path.exists(path):
        return []  # no memory yet
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(document_id: str, question: str, answer: str):
    """
    Append a new turn to memory:
    {
        "role": "user",
        "content": question
    },
    {
        "role": "assistant",
        "content": answer
    }

    And keep only last MAX_TURNS.
    """
    path = get_memory_path(document_id)

    memory = load_memory(document_id)

    # Append new user + assistant turns
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": answer})

    # Keep only last MAX_TURNS entries
    memory = memory[-MAX_TURNS:]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def format_memory_for_prompt(memory: List[Dict]) -> str:
    """
    Convert memory list into a nice prompt-ready string:
    User: Hi
    Assistant: Hello!
    """
    if not memory:
        return ""

    result = []
    for turn in memory:
        role = turn["role"].capitalize()
        content = turn["content"]
        result.append(f"{role}: {content}")

    return "\n".join(result)
