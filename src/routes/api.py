from __future__ import annotations

import fastapi

from ..utils.models import User, UserModel
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
        res.set_cookie(key="session", value=request.headers.get("username"))
        return res
