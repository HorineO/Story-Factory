# Pydantic v2 moved `BaseSettings` to `pydantic_settings` package. Keep backward compatibility.
try:
    from pydantic_settings import BaseSettings  # type: ignore  # pylint: disable=import-error
except ImportError:  # Fallback for Pydantic v1
    from pydantic import BaseSettings  # type: ignore

from pydantic import Field
import os
from typing import Optional

class Settings(BaseSettings):  # type: ignore[misc]
    """Project configuration loaded from environment variables."""

    debug: bool = Field(default=True, description="Enable debug mode")
    port: int = Field(default=5000, description="Application port")
    api_prefix: str = Field(default="/api", description="API prefix")
    static_folder: str = Field(default="../frontend/build", description="Static folder path")
    static_url_path: str = Field(default="/", description="Static URL path")
    socketio_cors: str = Field(default="*", description="Allowed CORS origins for Socket.IO")

    # OpenAI config
    openai_base_url: str = Field(default="https://xiaohumini.site/v1", description="OpenAI endpoint")
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    default_model: str = Field(default="gpt-4o-mini", description="Default model name")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 