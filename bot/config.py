from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    telegram_bot_token: str
    groq_api_key: str = ""
    openai_api_key: str = ""
    llm_provider: str = "auto"
    groq_model: str = "llama-3.3-70b-versatile"
    openai_model: str = "gpt-4o-mini"
    webhook_url: str = ""
    webhook_secret: str = ""
    port: int = 8080
    admin_user_ids: str = ""
    database_path: str = "./data/tendem_demo.db"

    @property
    def admin_ids(self) -> set[int]:
        ids: set[int] = set()
        for part in self.admin_user_ids.split(","):
            part = part.strip()
            if part.isdigit():
                ids.add(int(part))
        return ids

    def resolve_llm(self) -> tuple[str, str, str] | None:
        if self.llm_provider == "groq" and self.groq_api_key:
            return ("groq", self.groq_api_key, self.groq_model)
        if self.llm_provider == "openai" and self.openai_api_key:
            return ("openai", self.openai_api_key, self.openai_model)
        if self.llm_provider == "auto":
            if self.groq_api_key:
                return ("groq", self.groq_api_key, self.groq_model)
            if self.openai_api_key:
                return ("openai", self.openai_api_key, self.openai_model)
        return None


settings = Settings()
