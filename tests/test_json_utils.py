from bot.src.misc.json_utils import orjson_dumps, orjson_loads


def test_orjson_roundtrip_simple():
    data = {"a": 1, "b": [1, 2, 3]}
    s = orjson_dumps(data)
    assert isinstance(s, str)
    assert orjson_loads(s) == data


def test_orjson_allows_non_str_keys():
    data = {1: "one", 2: "two"}
    s = orjson_dumps(data)
    parsed = orjson_loads(s)
    # non-str keys become strings in JSON
    assert parsed == {"1": "one", "2": "two"}


