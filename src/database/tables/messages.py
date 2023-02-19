from __future__ import annotations

from src.utils.models import Comment

from ._table import Table


class Comments(Table):
    async def setup(self) -> None:
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS comments "
            "(id TEXT,"
            " username TEXT,"
            " comment TEXT,"
            " comment_id UUID,"
            " created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            " FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,"
            " PRIMARY KEY (id, username))"
        )

    async def get_comments(self, id_: str) -> list[Comment] | None:
        data = await self.db.fetch("SELECT * FROM comments WHERE id = $1", id_)
        if data is None:
            return None
        return [Comment(*row) for row in data]

    async def create_comment(self, comment: Comment) -> None:
        await self.db.execute(
            "INSERT INTO comments (id, username, comment, comment_id) VALUES ($1, $2, $3, $4)",
            comment.id,
            comment.username,
            comment.comment,
            comment.comment_id,
        )

    async def delete_comment(self, id_: str, username: str, comment_id: str) -> None:
        await self.db.execute(
            "DELETE FROM comments WHERE id = $1 AND username = $2 AND comment_id = $3",
            id_,
            username,
            comment_id,
        )

    async def delete_comments(self, id_: str) -> None:
        await self.db.execute("DELETE FROM comments WHERE id = $1", id_)

    async def update_comment(self, id_: str, username: str, comment: str, comment_id: str) -> None:
        await self.db.execute(
            "UPDATE comments SET comment = $1 WHERE id = $2 AND username = $3 AND comment_id = $4",
            comment,
            id_,
            username,
            comment_id,
        )
