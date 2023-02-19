from __future__ import annotations

import datetime
import typing as t

from src.utils.models import Config as ConfigModel

from ._table import Table

if t.TYPE_CHECKING:
    import uuid


__all__: tuple[str, ...] = ("Config",)


class Config(Table):
    async def setup(self) -> None:
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS config "
            "(id BIGINT,"
            " migrations UUID [],"
            " last_update TIMESTAMP,"
            " PRIMARY KEY (id))"
        )

    async def get_config(self, bot_id: int) -> ConfigModel:
        data = await self.db.fetchrow("SELECT * FROM config WHERE id = $1", bot_id)
        if data is None:
            stamp = datetime.datetime.now()
            ids: list["uuid.UUID"] = []
            args = (bot_id, ids, stamp)
            await self.db.execute(
                "INSERT INTO config (id, migrations, last_update) VALUES ($1, $2, $3)",
                *args,
            )
            return ConfigModel(*args)
        return ConfigModel(*data)

    async def update_migration(self, bot_id: int, migration: "uuid.UUID") -> None:
        await self.db.execute(
            "UPDATE config SET migrations = array_append(migrations, $1) WHERE id = $2",
            migration,
            bot_id,
        )

    async def update_database(
        self, bot_id: int, stamp: datetime.datetime = datetime.datetime.now()
    ) -> None:
        await self.db.execute(
            "UPDATE config SET last_update = $1 WHERE id = $2", stamp, bot_id
        )
