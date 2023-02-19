from __future__ import annotations


import fastapi

from . import Extension, route


class Home(Extension):
    @route("/", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        session = request.cookies.get("session")
        if session is not None and session in [i.username for i in self.app.users]:
            return self.app.templates.TemplateResponse(
                "index.html", {"request": request, "name": "Home", "users": True}
            )
        return self.app.templates.TemplateResponse(
            "index.html", {"request": request, "name": "Home", "users": False}
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
        return self.app.templates.TemplateResponse(
            "index.html", {"request": request, "name": "Home", "users": False}
        )

    @route("/novel", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def novel(self, request: fastapi.Request, novel_id: int) -> fastapi.responses.Response:
        if novel_id not in self.app.novels:
            return self.app.templates.TemplateResponse(
                "error.html", {"request": request, "name": "Error"}
            )
        novel = self.app.novels[novel_id]
        return self.app.templates.TemplateResponse("template.html", {"request": request, "name": novel.name, "anime": novel})


