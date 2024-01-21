import os
from typing import Any


def get(value: Any, name: str):
    return value if value else os.environ[name]
