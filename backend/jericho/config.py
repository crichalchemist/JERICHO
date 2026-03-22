"""
Application settings loaded from environment variables / .env file.
All external config goes through this module — nothing reads os.environ directly.
"""
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # State persistence (Phase 0: JSON file; Phase 2: replaced by Supabase)
    state_path: Path = Field(
        default=Path("../src/data/state_good.json"),
        description="Path to JSON state file (Phase 0 only).",
    )

    # Supabase (Phase 2+)
    supabase_url: str = Field(default="", description="Supabase project URL.")
    supabase_anon_key: str = Field(default="", description="Supabase anonymous key.")
    supabase_service_role_key: str = Field(default="", description="Supabase service-role key.")

    # LLM (Phase 1+)
    ollama_host: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3-8b")

    # Security
    jwt_secret: str = Field(default="changeme")
    credential_encryption_key: str = Field(default="")

    # OpenTelemetry (Phase 1+)
    # Empty string → console exporter (local dev). Set to OTLP endpoint in prod.
    otel_exporter_otlp_endpoint: str = Field(default="")
    otel_service_name: str = Field(default="jericho-backend")

    # Server
    port: int = Field(default=8000)

    # Model registry
    model_registry_path: Path = Field(
        default=Path(__file__).parent.parent / "config" / "model_registry.yaml",
    )


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return a cached Settings instance (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
