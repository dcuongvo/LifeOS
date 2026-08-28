from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LifeOS"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"

    ollama_host: str = "http://172.27.80.1:11434"
    embedding_model: str = "qwen3-embedding:4b"
    chat_model: str = "qwen3:8b"

    qdrant_path: str = "data/qdrant"
    learning_collection: str = "learning_memories"
    embedding_vector_size: int = 2560

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()