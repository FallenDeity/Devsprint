from __future__ import annotations

import fastapi

from ..utils.models import Comment, User, UserModel
from . import Extension, route


class Api(Extension):
    @route("/api/v1/signup", method="POST", response_model=fastapi.responses.JSONResponse)
    async def signup(self, data: UserModel) -> fastapi.responses.Response:
        username, password = data.username, data.password
        user = await self.app.db.user.get_user(username)
        if user is not None:
            return fastapi.responses.JSONResponse({"message": "Username already exists"}, status_code=400)
        await self.app.db.user.create_user(User(username, password))
        return fastapi.responses.JSONResponse({"message": "User created"}, status_code=201)

    @route("/api/v1/login", method="POST", response_model=fastapi.responses.Response)
    async def login(self, data: UserModel) -> fastapi.responses.Response:
        username, password = data.username, data.password
        user = await self.app.db.user.get_user(username)
        if user is None:
            return fastapi.responses.JSONResponse({"message": "Username does not exist"}, status_code=400)
        if user.password != password:
            return fastapi.responses.JSONResponse({"message": "Incorrect password"}, status_code=400)
        self.app.users.append(data)
        return fastapi.responses.JSONResponse({"message": "Logged in"}, status_code=200)

    @route("/api/v1/redirect", method="GET", response_model=fastapi.responses.Response)
    async def redirect(self, request: fastapi.Request) -> fastapi.responses.Response:
        res = fastapi.responses.RedirectResponse(url="/")
        res.set_cookie(key="session", value=request.headers.get("username", ""))
        return res

    @route("/api/v1/comment", method="POST", response_model=fastapi.responses.JSONResponse)
    async def comment(self, data: dict[str, str]) -> fastapi.responses.JSONResponse:
        print(data)
        comment = Comment.from_payload(data)
        await self.app.db.comments.create_comment(comment)
        return fastapi.responses.JSONResponse({"message": "Comment created"}, status_code=201)

    @route("/api/v1/bookmark", method="POST", response_model=fastapi.responses.JSONResponse)
    async def bookmark(self, data: dict[str, str]) -> fastapi.responses.JSONResponse:
        username, post_id = data["username"], int(data["id"])
        bookmarks = (await self.app.db.user.get_bookmarks(username)) or []
        if post_id in bookmarks:
            await self.app.db.user.remove_bookmark(username, post_id)
            return fastapi.responses.JSONResponse({"message": "Bookmark removed"}, status_code=200)
        await self.app.db.user.add_bookmark(username, post_id)
        return fastapi.responses.JSONResponse({"message": "Bookmark added"}, status_code=201)

    @route("/api/v1/avatar", method="POST", response_model=fastapi.responses.JSONResponse)
    async def avatar(self, data: dict[str, str]) -> fastapi.responses.JSONResponse:
        username, avatar = data["username"], data["avatar"]
        await self.app.db.user.update_avatar(username, avatar)
        return fastapi.responses.JSONResponse({"message": "Avatar updated"}, status_code=200)
