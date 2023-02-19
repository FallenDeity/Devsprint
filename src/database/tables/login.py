from src.utils.models import User as UserModel, Comment

from ._table import Table


class User(Table):

    async def setup(self) -> None:
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT,"
            " password TEXT,"
            " avatar TEXT,"
            " bookmarks BIGINT [],"
            " created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            " PRIMARY KEY (username))"
        )

    async def get_user(self, username: str) -> UserModel | None:
        data = await self.db.fetchrow("SELECT * FROM users WHERE username = $1", username)
        if data is None:
            return None
        return UserModel(*data)

    async def create_user(self, user: UserModel) -> None:
        await self.db.execute(
            "INSERT INTO users (username, password, avatar, bookmarks) VALUES ($1, $2, $3, $4)",
            user.username, user.password, user.avatar, user.bookmarks
        )

    async def delete_user(self, username: str) -> None:
        await self.db.execute("DELETE FROM users WHERE username = $1", username)

    async def get_bookmarks(self, username: str) -> list[int] | None:
        data = await self.db.fetchrow("SELECT bookmarks FROM users WHERE username = $1", username)
        if data is None:
            return None
        return data[0]

    async def add_bookmark(self, username: str, post_id: int) -> None:
        await self.db.execute(
            "UPDATE users SET bookmarks = array_append(bookmarks, $1) WHERE username = $2", post_id, username
        )

    async def remove_bookmark(self, username: str, post_id: int) -> None:
        await self.db.execute(
            "UPDATE users SET bookmarks = array_remove(bookmarks, $1) WHERE username = $2", post_id, username
        )

    async def update_avatar(self, username: str, avatar: str) -> None:
        await self.db.execute("UPDATE users SET avatar = $1 WHERE username = $2", avatar, username)

    async def get_comments(self, username: str) -> list[Comment] | None:
        data = await self.db.fetch("SELECT * FROM comments WHERE username = $1", username)
        if data is None:
            return None
        return [Comment(*row) for row in data]
