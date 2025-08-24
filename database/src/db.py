from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


class Base(DeclarativeBase):
    pass


def create_engine_from_dsn(dsn: str):
    return create_engine(dsn, pool_pre_ping=True, future=True)


def get_session_factory(dsn: str) -> sessionmaker[Session]:
    engine = create_engine_from_dsn(dsn)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def create_all(base: type[Base], dsn: str) -> None:
    engine = create_engine_from_dsn(dsn)
    base.metadata.create_all(engine)


@contextmanager
def session_scope(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def session_generator(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    with session_scope(session_factory) as session:
        yield session
