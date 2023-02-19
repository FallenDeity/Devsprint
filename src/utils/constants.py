from __future__ import annotations

import enum
import pathlib
import typing

__all__: tuple[str, ...] = ("PATHS",)


class BaseEnum(enum.Enum):
    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        return self.value


class PATHS(BaseEnum):
    SOURCE = pathlib.Path("src")
    UTILS = pathlib.Path("src") / "utils"
    ROUTES = pathlib.Path("src") / "routes"
    CLIENT = pathlib.Path("client") / "client"
    STATIC = pathlib.Path("src") / "templates" / "static"
    TEMPLATES = pathlib.Path("src") / "templates"
    ASSETS = pathlib.Path("src") / "templates" / "static" / "assets"

    def __str__(self) -> str:
        return str(self.value.as_posix())
