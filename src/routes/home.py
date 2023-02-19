from __future__ import annotations

import random

import fastapi

from ..utils.constants import PATHS
from . import Extension, route


class Home(Extension):
    @route("/", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = random.choice(
            [
                i.as_posix().split("/static")[-1]
                for i in (PATHS.ASSETS / "footers").glob("*.jpg")
            ]
        )
        animes = random.sample(list(self.app.animes.values()), k=20)
        chunks = [animes[i : i + 5] for i in range(0, len(animes), 5)]
        session = request.cookies.get("session")
        if session is not None and session in [i.username for i in self.app.users]:
            return self.app.templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "name": "Home",
                    "users": True,
                    "f_img": f_img,
                    "animes": chunks,
                    "str": str,
                },
            )
        return self.app.templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "name": "Home",
                "users": False,
                "f_img": f_img,
                "animes": chunks,
                "str": str,
            },
        )

    @route("/login", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def login(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "login.html", {"request": request, "name": "Login"}
        )

    @route("/signup", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def signup(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "signup.html", {"request": request, "name": "Signup"}
        )

    @route("/logout", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def logout(self, request: fastapi.Request) -> fastapi.responses.Response:
        name = request.cookies.pop("session")
        self.app.users.remove([i for i in self.app.users if i.username == name][0])
        return fastapi.responses.RedirectResponse("/")

    @route("/source", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def source(self, _: fastapi.Request) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(
            url="https://github.com/FallenDeity/Devsprint"
        )

    @route("/email", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def source(self, _: fastapi.Request) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(
            url="mailto:triyanmukherjee@gmail.com"
        )

    @route("/profile", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def source(self, request: fastapi.Request) -> fastapi.responses.Response:
        session = request.cookies.get("session")
        user = await self.app.db.user.get_user(session)
        user.avatar = f"assets/avatars/{random.randint(1, 3)}.png"
        return self.app.templates.TemplateResponse(
            "profile.html", {"request": request, "user": user, "users": True}
        )

    @route(
        "/novel/{novel_id}",
        response_model=fastapi.responses.RedirectResponse,
        method="GET",
    )
    async def novel(
        self, _: fastapi.Request, novel_id: int
    ) -> fastapi.responses.RedirectResponse:
        return fastapi.responses.RedirectResponse(f"/novel?novel_id={novel_id}")

    @route("/novel", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def novel(
        self, request: fastapi.Request, novel_id: int
    ) -> fastapi.responses.Response:
        if novel_id not in self.app.animes:
            return self.app.templates.TemplateResponse(
                "error.html", {"request": request, "name": "Error"}
            )
        anime = self.app.animes[novel_id]
        return self.app.templates.TemplateResponse(
            "template.html", {"request": request, "anime": anime}
        )
