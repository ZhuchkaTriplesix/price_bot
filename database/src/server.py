from __future__ import annotations

import asyncio

import grpc
from pydantic_settings import BaseSettings

from .db import Base, get_session_factory, session_scope, create_all
from .repository import UserRepository, ItemRepository, LogRepository

from database.proto import database_pb2, database_pb2_grpc  # type: ignore


class Settings(BaseSettings):
    DATABASE_DSN: str
    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 50051


class DatabaseService(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def ChangeAccess(self, request, context):
        with session_scope(self._session_factory) as session:
            ok = UserRepository.change_access(
                session, int(request.telegram_id), int(request.group_id)
            )
            return database_pb2.ChangeAccessResponse(ok=ok)

    def IsOwner(self, request, context):
        with session_scope(self._session_factory) as session:
            ok = UserRepository.is_owner(session, int(request.telegram_id))
            return database_pb2.IsAccessResponse(ok=ok)

    def IsAdmin(self, request, context):
        with session_scope(self._session_factory) as session:
            ok = UserRepository.is_admin(session, int(request.telegram_id))
            return database_pb2.IsAccessResponse(ok=ok)

    def DeleteItem(self, request, context):
        with session_scope(self._session_factory) as session:
            ok = ItemRepository.delete_item(
                session, int(request.telegram_id), request.hash_name
            )
            return database_pb2.DeleteItemResponse(ok=ok)

    def UserItems(self, request, context):
        with session_scope(self._session_factory) as session:
            items = ItemRepository.user_items(session, int(request.telegram_id))
            return database_pb2.UserItemsResponse(items=items)

    def AddLog(self, request, context):
        with session_scope(self._session_factory) as session:
            LogRepository.add(
                session,
                int(request.telegram_id),
                request.username or None,
                request.function_name,
            )
            return database_pb2.AddLogResponse(ok=True)


async def serve() -> None:
    settings = Settings()  # type: ignore[call-arg]
    create_all(Base, settings.DATABASE_DSN)
    session_factory = get_session_factory(settings.DATABASE_DSN)

    server = grpc.aio.server()
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(
        DatabaseService(session_factory), server
    )
    listen_addr = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
