from __future__ import annotations

import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    username: Mapped[str | None] = mapped_column(String(length=32))
    group_id: Mapped[int] = mapped_column(Integer, default=0)
    created_date: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)


class Items(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    hash_name: Mapped[str] = mapped_column(String(length=60))
    item_count: Mapped[int] = mapped_column(Integer)


class LogBase(Base):
    __tablename__ = "functions_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    username: Mapped[str | None] = mapped_column(String(length=32))
    function_name: Mapped[str] = mapped_column(String(length=12))
    time_used: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)


