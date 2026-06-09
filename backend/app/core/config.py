from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic AI Insurance Policy Analyzer"
    frontend_origin: str = Field(default="http://localhost:3000", alias="FRONTEND_ORIGIN")

    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_anon_key: str = Field(alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_jwt_secret: str | None = Field(default=None, alias="SUPABASE_JWT_SECRET")
    supabase_storage_bucket: str = Field(default="policies", alias="SUPABASE_STORAGE_BUCKET")

    llm_provider: str = Field(default="deepseek", alias="LLM_PROVIDER")
    deepseek_api_key: str = Field(alias="DEEPSEEK_API_KEY")
    deepseek_api_url: str = Field(
        default="https://api.deepseek.com/v1/chat/completions",
        alias="DEEPSEEK_API_URL",
    )
    deepseek_model: str = Field(default="deepseek-chat", alias="DEEPSEEK_MODEL")

    claude_api_key: str | None = Field(default=None, alias="CLAUDE_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

