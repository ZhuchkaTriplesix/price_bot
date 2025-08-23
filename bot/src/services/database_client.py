from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

import grpc

from database.proto import database_pb2, database_pb2_grpc  # type: ignore


@dataclass(slots=True)
class DatabaseClient:
    target: str

    def __post_init__(self) -> None:
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[database_pb2_grpc.DatabaseServiceStub] = None

    async def start(self) -> None:
        if self.channel is None:
            self.channel = grpc.aio.insecure_channel(self.target)
            self.stub = database_pb2_grpc.DatabaseServiceStub(self.channel)

    async def stop(self) -> None:
        if self.channel is not None:
            await self.channel.close()
            self.channel = None
            self.stub = None

    async def change_access(self, telegram_id: int, group_id: int) -> bool:
        assert self.stub is not None
        resp = await self.stub.ChangeAccess(database_pb2.ChangeAccessRequest(telegram_id=telegram_id, group_id=group_id))
        return bool(resp.ok)

    async def is_owner(self, telegram_id: int) -> bool:
        assert self.stub is not None
        resp = await self.stub.IsOwner(database_pb2.IsAccessRequest(telegram_id=telegram_id))
        return bool(resp.ok)

    async def is_admin(self, telegram_id: int) -> bool:
        assert self.stub is not None
        resp = await self.stub.IsAdmin(database_pb2.IsAccessRequest(telegram_id=telegram_id))
        return bool(resp.ok)

    async def delete_item(self, telegram_id: int, hash_name: str) -> bool:
        assert self.stub is not None
        resp = await self.stub.DeleteItem(database_pb2.DeleteItemRequest(telegram_id=telegram_id, hash_name=hash_name))
        return bool(resp.ok)

    async def user_items(self, telegram_id: int) -> Dict[str, int]:
        assert self.stub is not None
        resp = await self.stub.UserItems(database_pb2.UserItemsRequest(telegram_id=telegram_id))
        return dict(resp.items)

    async def add_log(self, telegram_id: int, username: Optional[str], function_name: str) -> None:
        assert self.stub is not None
        await self.stub.AddLog(database_pb2.AddLogRequest(telegram_id=telegram_id, username=username or "", function_name=function_name))


