from __future__ import annotations

from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram
    TOKEN: str = Field(..., description="Telegram bot token")

    # Access control (kept in env for now; DB will be moved to another service later)
    OWNER_IDS: List[int] = Field(default_factory=list, description="List of owner user IDs")
    ADMIN_IDS: List[int] = Field(default_factory=list, description="List of admin user IDs")

    # External services
    DATABASE_GRPC_ADDR: str | None = Field(default=None, description="database gRPC address, e.g. database:50051")

    @field_validator("OWNER_IDS", "ADMIN_IDS", mode="before")
    @classmethod
    def parse_int_list(cls, value: str | list[int] | None) -> list[int]:
        if value is None:
            return []
        if isinstance(value, list):
            return [int(v) for v in value]
        if isinstance(value, str):
            if not value.strip():
                return []
            return [int(x.strip()) for x in value.split(",") if x.strip()]
        return []


settings = Settings()


