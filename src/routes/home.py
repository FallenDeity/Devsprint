from __future__ import annotations

import random

import fastapi

from ..utils.constants import PATHS
from . import Extension, route


class Home(Extension):
    @route("/", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        f_img = random.choice([i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / "footers").glob("*.jpg")])
        animes = {k: v for k, v in sorted(self.app.animes.items(), key=lambda x: x[1].rank) if v.trailer.embed_url}
        animes = random.sample(list(animes.values()), k=20)
        chunks = [animes[i : i + 5] for i in range(0, len(animes), 5)]
        session = request.cookies.get("session", "")
        users = await self.app.db.user.get_user(session)
        return self.app.templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "name": "Home",
                "users": users,
                "f_img": f_img,
                "animes": chunks,
                "str": str,
            },
        )

    @route("/login", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def login(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse("login.html", {"request": request, "name": "Login"})

    @route("/signup", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def signup(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse("signup.html", {"request": request, "name": "Signup"})

    @route("/logout", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def logout(self, request: fastapi.Request) -> fastapi.responses.Response:
        name = request.cookies.pop("session")
        to_remove = [i for i in self.app.users if i.username == name][0]
        self.app.users.remove(to_remove)
        return fastapi.responses.RedirectResponse("/")

    @route("/source", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def source(self, _: fastapi.Request) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(url="https://github.com/FallenDeity/Devsprint")

    @route("/email", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def mail(self, _: fastapi.Request) -> fastapi.responses.Response:
        return fastapi.responses.RedirectResponse(url="mailto:triyanmukherjee@gmail.com")

    @route("/profile", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def profile(self, request: fastapi.Request) -> fastapi.responses.Response:
        session = request.cookies.get("session", "")
        user = await self.app.db.user.get_user(session)
        assert user is not None
        user.bookmarks = [self.app.animes[i] for i in user.bookmarks]  # type: ignore
        f_img = random.choice([i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / "footers").glob("*.jpg")])
        return self.app.templates.TemplateResponse(
            "profile.html", {"request": request, "user": user, "users": user, "f_img": f_img, "name": "Profile"}
        )

    @route("/anime", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def novel(self, request: fastapi.Request, anime_id: int) -> fastapi.responses.Response:
        f_img = random.choice([i.as_posix().split("/static")[-1] for i in (PATHS.ASSETS / "footers").glob("*.jpg")])
        user = request.cookies.get("session", "")
        users = await self.app.db.user.get_user(user)
        if anime_id not in self.app.animes:
            return self.app.templates.TemplateResponse("error.html", {"request": request, "name": "Error"})
        anime = self.app.animes[anime_id]
        comments = await self.app.db.comments.get_comments(str(anime.mal_id))
        return self.app.templates.TemplateResponse(
            "template.html",
            {"request": request, "anime": anime, "users": users, "f_img": f_img, "comments": comments, "name": "Anime"},
        )
