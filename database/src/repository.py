from __future__ import annotations

from typing import Dict, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .models import Users, Items, LogBase


class UserRepository:
    @staticmethod
    def get_by_telegram_id(session: Session, telegram_id: int) -> Users | None:
        return session.execute(select(Users).where(Users.telegram_id == telegram_id)).scalar_one_or_none()

    @staticmethod
    def add_user(session: Session, telegram_id: int, username: str | None) -> Users:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        if user is None:
            user = Users(telegram_id=telegram_id, username=username)
            session.add(user)
        return user

    @staticmethod
    def change_access(session: Session, telegram_id: int, group_id: int) -> bool:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        if user is None:
            return False
        user.group_id = group_id
        return True

    @staticmethod
    def is_owner(session: Session, telegram_id: int) -> bool:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        return bool(user and user.group_id >= 3)

    @staticmethod
    def is_admin(session: Session, telegram_id: int) -> bool:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        return bool(user and user.group_id >= 2)


class ItemRepository:
    @staticmethod
    def delete_item(session: Session, telegram_id: int, hash_name: str) -> bool:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        if user is None:
            return False
        q = (
            delete(Items)
            .where(Items.user_id == user.id)
            .where(Items.hash_name == hash_name)
        )
        result = session.execute(q)
        return result.rowcount > 0

    @staticmethod
    def user_items(session: Session, telegram_id: int) -> Dict[str, int]:
        user = UserRepository.get_by_telegram_id(session, telegram_id)
        if user is None:
            return {}
        rows = session.execute(select(Items).where(Items.user_id == user.id)).scalars().all()
        out: Dict[str, int] = {}
        for item in rows:
            out[item.hash_name] = item.item_count
        return out


class LogRepository:
    @staticmethod
    def add(session: Session, telegram_id: int, username: Optional[str], function_name: str) -> None:
        session.add(LogBase(telegram_id=telegram_id, username=username, function_name=function_name))


