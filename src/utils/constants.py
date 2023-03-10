from __future__ import annotations

import enum
import pathlib
import typing

__all__: tuple[str, ...] = ("PATHS", "BOT_ID", "AVATAR")
BOT_ID: int = 1005755826994163733
AVATAR: list[str] = [
    "https://www.w3schools.com/howto/img_avatar.png",
    "https://www.w3schools.com/howto/img_avatar2.png",
    "https://www.w3schools.com/w3images/avatar2.png",
    "https://www.w3schools.com/w3images/avatar5.png",
    "https://www.w3schools.com/w3images/avatar6.png",
]


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
    TABLES = pathlib.Path("src") / "database" / "tables"
    MIGRATIONS = pathlib.Path("src") / "database" / "migrations"

    def __str__(self) -> str:
        return str(self.value.as_posix())
