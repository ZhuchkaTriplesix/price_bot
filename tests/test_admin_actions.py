import importlib

import pytest

from bot.src.handlers.admin import action


@pytest.fixture(autouse=True)
def configure_env(monkeypatch):
    monkeypatch.setenv("OWNER_IDS", "[1,2]")
    monkeypatch.setenv("ADMIN_IDS", "[3,4]")
    # Reload settings and then action so env is applied
    import bot.src.config as cfg
    importlib.reload(cfg)
    importlib.reload(action)


def test_owner_access_allowed():
    result = action.check_owner_access(1)
    assert result.is_allowed is True


def test_owner_access_denied():
    result = action.check_owner_access(99)
    assert result.is_allowed is False
    assert "нет доступа" in (result.error or "")


@pytest.mark.parametrize("user_id,allowed", [(3, True), (4, True), (1, True), (99, False)])
def test_admin_access(user_id, allowed):
    result = action.check_admin_access(user_id)
    assert result.is_allowed is allowed


@pytest.mark.asyncio
async def test_action_messages():
    assert "Vip" in await action.give_vip(action.TelegramIdPayload(telegram_id=5))
    assert "выдали" in await action.add_admin(action.TelegramIdPayload(telegram_id=5))
    assert "удалили админ" in await action.delete_admin(action.TelegramIdPayload(telegram_id=5))
    assert "удалили предмет" in await action.delete_item(action.DeleteItemPayload(telegram_id=5, hash_name="x"))


