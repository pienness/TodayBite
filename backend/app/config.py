from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM 配置
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_API_BASE: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
