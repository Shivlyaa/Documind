# app/routes/chat.py

import requests
from typing import Optional
from app.core.config import settings


class HFLLM:
    def __init__(self, timeout: int = 60):
        """
        Uses Hugging Face Router (OpenAI-compatible) chat completions endpoint.
        Requires a token created with 'Make calls to Inference Providers' permission.
        """
        self.base_url = settings.HF_API_BASE.rstrip("/")
        self.model = settings.LLM_MODEL
        self.token = settings.HF_TOKEN
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        # OpenAI-compatible chat completions endpoint on HF router
        self.chat_url = f"{self.base_url}/chat/completions"

    def invoke(self, prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
        """
        Send a single-user message as a chat completion and return the model reply as a string.
        Falls back to several common response shapes to be robust across providers.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }

        try:
            resp = requests.post(self.chat_url, headers=self.headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            # Wrap for consistent upstream handling
            raise RuntimeError(f"HF request failed: {e}")

        # parse JSON safely
        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError("HF response is not valid JSON")

        # Common shape for OpenAI-compatible responses
        # Try to extract in order of likelihood
        # 1) choices[0].message.content (chat completion)
        choices = data.get("choices")
        if isinstance(choices, list) and len(choices) > 0:
            first = choices[0]
            # chat-style
            message = first.get("message") if isinstance(first, dict) else None
            if isinstance(message, dict) and "content" in message:
                return message["content"]
            # fallback to text field
            for k in ("text", "content", "message"):
                if isinstance(first, dict) and k in first:
                    return first[k]
            # sometimes choices[0].delta / text exists
            if isinstance(first, dict) and "delta" in first and isinstance(first["delta"], dict):
                if "content" in first["delta"]:
                    return first["delta"]["content"]

        # 2) Some providers return 'generated_text' or outputs list
        if "generated_text" in data:
            return data["generated_text"]

        if "output" in data and isinstance(data["output"], list) and len(data["output"]) > 0:
            out = data["output"][0]
            if isinstance(out, dict) and "generated_text" in out:
                return out["generated_text"]
            if isinstance(out, str):
                return out

        # 3) fallback: try to stringify the whole response safely
        raise RuntimeError(f"Unable to parse HF response: {data}")


# singleton helper
def get_llm():
    return HFLLM()
