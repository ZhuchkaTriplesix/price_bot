from __future__ import annotations

from typing import Any

import orjson


def orjson_dumps(data: Any) -> str:
    return orjson.dumps(
        data, option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS
    ).decode()


def orjson_loads(data: str | bytes | bytearray) -> Any:
    return orjson.loads(data)
