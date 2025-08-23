import importlib

import pytest


@pytest.mark.parametrize(
    "env_owner,env_admin,expected_owner,expected_admin",
    [
        ("[1,2]", "[3,4]", [1, 2], [3, 4]),
        ("[]", "[]", [], []),
        (None, None, [], []),
    ],
)
def test_settings_list_parsing(monkeypatch, env_owner, env_admin, expected_owner, expected_admin):
    monkeypatch.setenv("TOKEN", "TEST")
    if env_owner is not None:
        monkeypatch.setenv("OWNER_IDS", env_owner)
    if env_admin is not None:
        monkeypatch.setenv("ADMIN_IDS", env_admin)
    import bot.src.config as cfg
    importlib.reload(cfg)
    assert cfg.settings.OWNER_IDS == expected_owner
    assert cfg.settings.ADMIN_IDS == expected_admin


