from __future__ import annotations

import importlib
import inspect
import pathlib
import typing as t

import _pickle as pickle
import aiohttp
import fastapi
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from ..database import Database
from ..routes import Extension
from ..utils.constants import PATHS
from ..utils.models import Anime
from .environment import config
from .logger import Logger

__author__: str = "Triyan Mukherjee"
__version__: str = "0.0.1"
__all__: tuple[str, ...] = ("Website",)


class Website(fastapi.FastAPI):
    client: aiohttp.ClientSession
    templates: Jinja2Templates = Jinja2Templates(directory=str(PATHS.TEMPLATES))
    _static: list[fastapi.routing.Mount] = [
        fastapi.routing.Mount(
            "/static",
            StaticFiles(directory=str(PATHS.STATIC), html=True),
            name="static",
        ),
        fastapi.routing.Mount(
            "/assets",
            StaticFiles(directory=str(PATHS.ASSETS), html=True),
            name="assets",
        ),
    ]
    users = []
    animes: dict[int, Anime] = {}

    def __init__(
        self,
        *,
        title: str = __author__,
        description: str = "",
        docs: str | None = None,
        redoc: str | None = None,
        debug: bool = False,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
            docs_url=docs,
            redoc_url=redoc,
            debug=debug,
            **kwargs,
        )
        self.logger = Logger(name=__name__, file=True)
        self.config = config
        self.db = Database(self)
        self.exception_handler(HTTPException)(self._exception_handler)

    def _mount_files(self) -> None:
        self.routes.extend(self._static)

    def _auto_setup(self, path: str) -> None:
        module = importlib.import_module(path)
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, Extension)
                and name != "Extension"
            ):
                router = obj(app=self)
                self.include_router(router)
                self.logger.info(f"Loaded {name} extension")

    async def _exception_handler(
        self, request: fastapi.Request, _exc: HTTPException
    ) -> fastapi.responses.Response:
        self.logger.error(f"Error: {_exc.detail}")
        return self.templates.TemplateResponse(
            "error.html", {"request": request, "name": "Error"}
        )

    def _load_files(self) -> None:
        self.logger.info("Loading extensions")
        path = t.cast(pathlib.Path, PATHS.ROUTES)
        for file in path.glob("*.py"):
            if file.name.startswith("_"):
                continue
            self._auto_setup(f"{path.parent}.{path.name}.{file.stem}")
        self.logger.info("Extensions loaded")

    async def on_startup(self) -> None:
        self.logger.info("Starting up...")
        self.client = aiohttp.ClientSession()
        self._mount_files()
        self._load_files()
        await self.db.setup()
        with open("data.pickle", "rb") as f:
            data = pickle.load(f)
        self.animes = {j.mal_id: j for i in data for j in i}
        self.logger.flair("Started up successfully.")

    async def on_shutdown(self) -> None:
        self.logger.flair("Shutting down...")
        await self.client.close()
        self.logger.error("Shut down successfully.")

    def run(self) -> None:
        self.logger.flair("Running...")
        uvicorn.run(
            "main:app",
            reload=True,
            reload_dirs=[str(PATHS.ROUTES), str(PATHS.TEMPLATES)],
            use_colors=True,
        )
