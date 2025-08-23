from __future__ import annotations

from pydantic import BaseModel, Field


class TelegramIdPayload(BaseModel):
    telegram_id: int = Field(..., ge=1)


class DeleteItemPayload(BaseModel):
    telegram_id: int = Field(..., ge=1)
    hash_name: str = Field(..., min_length=1)


