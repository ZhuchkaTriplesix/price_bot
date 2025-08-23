import pytest
from pydantic import ValidationError

from bot.src.handlers.admin.schemas import TelegramIdPayload, DeleteItemPayload


def test_telegram_id_payload_valid():
    payload = TelegramIdPayload(telegram_id=123)
    assert payload.telegram_id == 123


def test_telegram_id_payload_invalid():
    with pytest.raises(ValidationError):
        TelegramIdPayload(telegram_id=0)


def test_delete_item_payload_valid():
    payload = DeleteItemPayload(telegram_id=1, hash_name="abc")
    assert payload.telegram_id == 1
    assert payload.hash_name == "abc"


@pytest.mark.parametrize("hash_name", ["", " "])
def test_delete_item_payload_invalid(hash_name):
    with pytest.raises(ValidationError):
        DeleteItemPayload(telegram_id=1, hash_name=hash_name)


