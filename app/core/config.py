# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """
    Global configuration settings for DocuMind backend.
    Automatically loads variables from .env file.
    """

    # --------------------------
    # HuggingFace / LLM Settings
    # --------------------------
    HF_TOKEN: str = Field(..., description="HuggingFace API Token")
    HF_API_BASE: str = Field(
        default="https://router.huggingface.co/v1",
        description="Hugging Face router base URL for Inference Providers (OpenAI-compatible)."
    )

    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model used for vectorizing chunks"
    )

    LLM_MODEL: str = Field(
        default="google/flan-t5-small",
        description="LLM model used for generating answers (provider-enabled model recommended)"
    )

    # --------------------------
    # Application settings
    # --------------------------
    APP_NAME: str = "DocuMind API"
    ENV: str = Field(default="development")

    # --------------------------
    # File storage paths
    # --------------------------
    STORAGE_BASE: str = "storage"
    USER_FILES: str = "storage/user_files"
    INDEX_DIR: str = "storage/faiss_indexes"

    # --------------------------
    # CORS origins (Framer)
    # --------------------------
    ALLOWED_ORIGINS: List[str] = ["*"]  # Later replace with your Framer domain

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Created a global settings instance accessible everywhere
settings = Settings()
