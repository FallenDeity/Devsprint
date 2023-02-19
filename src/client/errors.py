from __future__ import annotations

__all__: tuple[str, ...] = ("UnicornException",)


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
