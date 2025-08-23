from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class TelegramIdPayload(BaseModel):
    telegram_id: int = Field(..., ge=1)


class DeleteItemPayload(BaseModel):
    telegram_id: int = Field(..., ge=1)
    hash_name: str = Field(..., min_length=1)

    @field_validator("hash_name")
    @classmethod
    def non_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("hash_name must not be blank")
        return v
