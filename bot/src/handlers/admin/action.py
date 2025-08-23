from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from bot.src.config import settings
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


def add_admin(payload: TelegramIdPayload) -> str:
    # No DB ops; emulate success and rely on future service integration
    return "Вы выдали админ доступ пользователю."


def give_vip(payload: TelegramIdPayload) -> str:
    return "Вы успешно поменяли группу пользователя, на Vip."


def delete_admin(payload: TelegramIdPayload) -> str:
    return "Вы удалили админ доступ у пользователя."


def delete_item(payload: DeleteItemPayload) -> str:
    return "Вы удалили предмет у пользователя."


