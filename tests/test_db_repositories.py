import os

import pytest
from sqlalchemy.orm import Session

from database.src.db import Base, create_all, get_session_factory, session_scope
from database.src.models import Users, Items
from database.src.repository import UserRepository, ItemRepository


PG_DSN = os.getenv(
    "TEST_DATABASE_DSN",
    "postgresql+psycopg://postgres:postgres@localhost:5432/pricebot",
)


@pytest.mark.integration
def test_user_and_items_flow_postgres():
    create_all(Base, PG_DSN)
    session_factory = get_session_factory(PG_DSN)

    with session_scope(session_factory) as session:
        assert isinstance(session, Session)
        # ensure user doesn't exist
        assert UserRepository.get_by_telegram_id(session, 99999) is None
        # add user
        UserRepository.add_user(session, 99999, "tester")
        session.flush()
        # change access
        assert UserRepository.change_access(session, 99999, 2) is True
        # add item row manually to then delete
        user = UserRepository.get_by_telegram_id(session, 99999)
        assert user is not None
        session.add(Items(user_id=user.id, hash_name="x", item_count=1))
        session.flush()
        # list items
        items = ItemRepository.user_items(session, 99999)
        assert items.get("x") == 1
        # delete
        assert ItemRepository.delete_item(session, 99999, "x") is True
