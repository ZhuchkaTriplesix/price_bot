import pytest

from bot.src.services.database_client import DatabaseClient


@pytest.mark.asyncio
async def test_db_client_fallback_methods_without_stubs():
    client = DatabaseClient("localhost:50051")
    # start/stop should not raise
    await client.start()
    await client.stop()
    # methods should return safe defaults without stubs
    assert await client.change_access(1, 2) is True
    assert await client.is_owner(1) is False
    assert await client.is_admin(1) is False
    assert await client.delete_item(1, "x") is True
    assert await client.user_items(1) == {}
    # add_log no return, should not raise
    await client.add_log(1, "user", "fn")
