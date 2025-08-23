from __future__ import annotations

from dataclasses import dataclass

from bot.src.config import settings
from bot.src.services.database_client import DatabaseClient
from .schemas import TelegramIdPayload, DeleteItemPayload


@dataclass(slots=True)
class AccessCheckResult:
    is_allowed: bool
    error: str | None = None


def _is_owner(user_id: int) -> bool:
    return user_id in set(settings.OWNER_IDS)


def _is_admin(user_id: int) -> bool:
    return user_id in set(settings.ADMIN_IDS) or _is_owner(user_id)


def check_owner_access(user_id: int) -> AccessCheckResult:
    if _is_owner(user_id):
        return AccessCheckResult(True)
    return AccessCheckResult(False, "У вас нет доступа к этой команде.")


def check_admin_access(user_id: int) -> AccessCheckResult:
    if _is_admin(user_id):
        return AccessCheckResult(True)
    return AccessCheckResult(False, "У вас нет доступа к этой команде.")


async def add_admin(payload: TelegramIdPayload) -> str:
    if settings.DATABASE_GRPC_ADDR:
        client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
        await client.start()
        await client.change_access(payload.telegram_id, 2)
        await client.stop()
    return "Вы выдали админ доступ пользователю."


async def give_vip(payload: TelegramIdPayload) -> str:
    if settings.DATABASE_GRPC_ADDR:
        client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
        await client.start()
        await client.change_access(payload.telegram_id, 1)
        await client.stop()
    return "Вы успешно поменяли группу пользователя, на Vip."


async def delete_admin(payload: TelegramIdPayload) -> str:
    if settings.DATABASE_GRPC_ADDR:
        client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
        await client.start()
        await client.change_access(payload.telegram_id, 0)
        await client.stop()
    return "Вы удалили админ доступ у пользователя."


async def delete_item(payload: DeleteItemPayload) -> str:
    if settings.DATABASE_GRPC_ADDR:
        client = DatabaseClient(settings.DATABASE_GRPC_ADDR)
        await client.start()
        await client.delete_item(payload.telegram_id, payload.hash_name)
        await client.stop()
    return "Вы удалили предмет у пользователя."
