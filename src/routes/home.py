import fastapi

from . import Extension, route


class Home(Extension):
    @route("/", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def home(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "index.html", {"request": request, "name": "Home"}
        )

    @route("/about", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def about(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "about.html", {"request": request, "name": "About"}
        )

    @route("/timeline", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def timeline(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "timeline.html", {"request": request, "name": "Timeline"}
        )

    @route("/sponsors", method="GET", response_model=fastapi.responses.HTMLResponse)
    async def sponsors(self, request: fastapi.Request) -> fastapi.responses.Response:
        return self.app.templates.TemplateResponse(
            "error.html", {"request": request, "name": "Sponsors"}
        )
