"""
Simple library to extract value from json.
Implemented in pure python.
"""

__version__ = "0.0.1"

import re
from typing import Any


def json_extract(data: Any, path: str) -> Any:
    """similar but not equal to the json_extract from sqlite3"""

    if data is None or path.startswith("."):
        return None

    if not path or path == "$":
        return data

    if "." in path:
        key, path = path.split(".", 1)
    else:
        key, path = path, ""

    idx = None
    m = re.search(r"^(.+?)\[(-?\d+)\]$", key)
    if m is not None:
        # Matching a list
        key, idx = m.group(1), int(m.group(2))

    if key == "$":
        value = data
    elif isinstance(data, dict):
        value = data.get(key)
    else:
        return None

    if idx is None:
        return json_extract(value, path)
    elif isinstance(value, list):
        try:
            return json_extract(value[idx], path)
        except IndexError:
            return None
    else:
        return None


if __name__ == "__main__":
    data = {"a": 2, "c": [4, 5, {"f": 7}], "x.y": 100}
    # It doesn't work when key has special characters such as "." and I
    # don't intend to fix it, since I probably never need to use such keys
    # in json.
    assert json_extract(data, '$."x.y"') is None
    assert json_extract(data, "$.x.y") is None
    assert json_extract(data, "$") == data
    assert json_extract(data, "") == data
    assert json_extract(data, "$.c") == [4, 5, {"f": 7}]
    assert json_extract(data, "c") == [4, 5, {"f": 7}]
    assert json_extract(data, "$.c[2]") == {"f": 7}
    assert json_extract(data, "$.c[2]x") is None
    assert json_extract(data, "$.c[2].f") == 7
    assert json_extract(data, "c[2].f") == 7
    assert json_extract(data, "$.c[-2]") == 5
    assert json_extract(data, "$.c[-3]") == 4
    assert json_extract(data, "$.c[3]") is None
    assert json_extract(data, "$.c[-4]") is None
    assert json_extract(data, "$.a") == 2
    assert json_extract(data, "$.x") is None
    assert json_extract({"a": "xyz"}, "$.a") == "xyz"
    assert json_extract({"a": "xyz"}, "a") == "xyz"
    assert json_extract({"a": "xyz"}, ".a") is None
    assert json_extract({"a": None}, "$.a") is None
    assert json_extract("xyz", "$") == "xyz"
    assert json_extract("xyz", "$.a") is None
    assert json_extract([1, 2, 3], "$[0]") == 1
    assert json_extract([1, 2, 3], "[0]") is None
    assert json_extract([1, 2, 3], ".[0]") is None
    assert json_extract(0, "$") == 0
    assert json_extract(0, "$.a") is None
    assert json_extract(True, "$") is True
