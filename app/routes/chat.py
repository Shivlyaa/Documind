# app/routes/chat.py

import requests
from app.core.config import settings


class HFLLM:
    """
    Wrapper for Hugging Face Router (OpenAI-compatible) Chat Completions API.
    Works with models like:
      - meta-llama/Llama-3-8b-instruct
      - mistralai/Mixtral-8x7B-Instruct
      - other OpenAI-format providers
    """

    def __init__(self, timeout: int = 60):
        self.base_url = settings.HF_API_BASE.rstrip("/")
        self.model = settings.LLM_MODEL
        self.token = settings.HF_TOKEN
        self.timeout = timeout

        # Required headers for OpenAI-style Chat Completions
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        # HF router OpenAI endpoint
        self.chat_url = f"{self.base_url}/chat/completions"

    def invoke(self, prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
        """
        Invoke the HF router with a system + user message.
        Returns the assistant response as a string.
        """

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, accurate RAG assistant. "
                        "Answer only using the provided document context. "
                        "Keep responses concise and factual."
                    )
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            resp = requests.post(
                self.chat_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()

        except requests.RequestException as e:
            # Unified error for upstream FastAPI
            raise RuntimeError(f"HF request failed: {e}")

        # Parse JSON
        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError("HF response is not valid JSON")

        # Expected OpenAI format:
        # { choices: [ { message: { role: 'assistant', content: '...' } } ] }
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            raise RuntimeError(f"Unable to parse HF response: {data}")


# Singleton helper
def get_llm():
    return HFLLM()
