from __future__ import annotations

import datetime
import random
import typing
import uuid
from abc import ABC

import attrs
from pydantic import BaseModel

from ..utils.constants import AVATAR

__all__: tuple[str, ...] = (
    "Model",
    "Config",
    "User",
    "Comment",
    "UserModel",
    "Anime",
)


class UserModel(BaseModel):
    ip: str
    username: str
    password: str


@attrs.define
class Model(ABC):
    """Base class for all models."""

    def to_payload(self) -> dict[typing.Any, typing.Any]:
        """Convert the model to a payload."""
        return attrs.asdict(self)


@attrs.define
class Comment(Model):
    id: str
    username: str
    avatar: str
    comment: str
    comment_id: uuid.UUID = attrs.field(factory=uuid.uuid4)
    created_at: datetime.datetime = attrs.field(factory=datetime.datetime.now)

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Comment:
        """Convert a payload to a model."""
        return cls(
            id=payload.get("id", ""),
            username=payload.get("username", ""),
            avatar=payload.get("avatar", ""),
            comment=payload.get("comment", ""),
            comment_id=payload.get("comment_id", uuid.uuid4()),
            created_at=payload.get("created_at", datetime.datetime.now()),
        )


@attrs.define
class Config(Model):
    id: int
    migrations: list[uuid.UUID]
    last_update: datetime.datetime


@attrs.define
class User(Model):
    username: str
    password: str
    avatar: str = random.choice(AVATAR)
    bookmarks: list[int] = attrs.field(factory=list)
    created_at: datetime.datetime = attrs.field(factory=datetime.datetime.now)

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> User:
        """Convert a payload to a model."""
        return cls(
            username=payload.get("username", ""),
            password=payload.get("password", ""),
            avatar=payload.get("avatar", AVATAR),
            bookmarks=payload.get("bookmarks", []),
        )


@attrs.define
class Image(Model):
    small: str
    large: str
    medium: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Image:
        """Convert a payload to a model."""
        return cls(
            small=payload.get("image_url", "") or "",
            medium=payload.get("small_image_url", "") or "",
            large=payload.get("large_image_url", "") or "",
        )


@attrs.define
class Images(Model):
    jpg: Image
    webp: Image

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Images:
        """Convert a payload to a model."""
        return cls(
            jpg=Image.from_payload(payload.get("jpg", {})),
            webp=Image.from_payload(payload.get("webp", {})),
        )


@attrs.define
class TrailerImage(Model):
    image_url: str
    small_image_url: str
    large_image_url: str
    medium_image_url: str
    maximum_image_url: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> TrailerImage:
        """Convert a payload to a model."""
        return cls(
            image_url=payload.get("image_url", "") or "",
            small_image_url=payload.get("small_image_url", "") or "",
            large_image_url=payload.get("large_image_url", "") or "",
            medium_image_url=payload.get("medium_image_url", "") or "",
            maximum_image_url=payload.get("maximum_image_url", "") or "",
        )


@attrs.define
class Trailer(Model):
    youtube_id: str
    url: str
    embed_url: str
    images: TrailerImage

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Trailer:
        """Convert a payload to a model."""
        return cls(
            youtube_id=payload.get("youtube_id", "") or "",
            url=payload.get("url", "") or "",
            embed_url=payload.get("embed_url", "") or "",
            images=TrailerImage.from_payload(payload.get("images", {})),
        )


@attrs.define
class TitleType(Model):
    type: str
    title: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> TitleType:
        """Convert a payload to a model."""
        return cls(
            type=payload.get("type", "") or "",
            title=payload.get("title", "") or "",
        )


@attrs.define
class Aired(Model):
    from_: str
    to: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Aired:
        """Convert a payload to a model."""
        return cls(
            from_=payload.get("from", "") or "",
            to=payload.get("to", "") or "",
        )


@attrs.define
class Broadcast(Model):
    day: str
    time: str
    timezone: str
    string: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Broadcast:
        """Convert a payload to a model."""
        return cls(
            day=payload.get("day", "") or "",
            time=payload.get("time", "") or "",
            timezone=payload.get("timezone", "") or "",
            string=payload.get("string", "") or "",
        )


@attrs.define
class Affiliate(Model):
    mal_id: int
    type: str
    name: str
    url: str

    @classmethod
    def from_payload(cls, payload: dict[typing.Any, typing.Any]) -> Affiliate:
        """Convert a payload to a model."""
        return cls(
            mal_id=payload.get("mal_id", 0) or 0,
            type=payload.get("type", "") or "",
            name=payload.get("name", "") or "",
            url=payload.get("url", "") or "",
        )


@attrs.define
class Anime(Model):
    mal_id: int
    url: str
    images: Images
    trailer: Trailer
    approved: bool
    title: str
    titles: list[TitleType]
    title_english: str
    title_japanese: str
    title_synonyms: list[str]
    type: str
    source: str
    episodes: int
    airing: bool
    aired: Aired
    duration: str
    rating: str
    score: float
    scored_by: int
    rank: int
    popularity: int
    members: int
    favorites: int
    synopsis: str
    background: str
    season: str
    year: int
    broadcast: Broadcast
    producers: list[Affiliate]
    licensors: list[Affiliate]
    studios: list[Affiliate]
    genres: list[Affiliate]
    explicit_genres: list[Affiliate]
    themes: list[Affiliate]
    demographic: list[Affiliate]

    @classmethod
    def from_payload(cls, data: dict[typing.Any, typing.Any]) -> Anime:
        return cls(
            mal_id=data.get("mal_id", 0) or 0,
            url=data.get("url", "") or "",
            images=Images.from_payload(data.get("images", {})),
            trailer=Trailer.from_payload(data.get("trailer", {})),
            approved=data.get("approved", False) or False,
            title=data.get("title", "") or "",
            titles=[TitleType.from_payload(title) for title in data.get("titles", [])],
            title_english=data.get("title_english", "") or "",
            title_japanese=data.get("title_japanese", "") or "",
            title_synonyms=data.get("title_synonyms", []) or [],
            type=data.get("type", "") or "",
            source=data.get("source", "") or "",
            episodes=data.get("episodes", 0) or 0,
            airing=data.get("airing", False),
            aired=Aired.from_payload(data.get("aired", {})),
            duration=data.get("duration", "") or "",
            rating=data.get("rating", "") or "",
            score=data.get("score", 0.0) or 0.0,
            scored_by=data.get("scored_by", 0) or 0,
            rank=data.get("rank", 0) or 0,
            popularity=data.get("popularity", 0) or 0,
            members=data.get("members", 0) or 0,
            favorites=data.get("favorites", 0) or 0,
            synopsis=data.get("synopsis", "") or "",
            background=data.get("background", "") or "",
            season=data.get("season", "") or "",
            year=data.get("year", 0) or 0,
            broadcast=Broadcast.from_payload(data.get("broadcast", {})),
            producers=[Affiliate.from_payload(producer) for producer in data.get("producers", [])],
            licensors=[Affiliate.from_payload(licensor) for licensor in data.get("licensors", [])],
            studios=[Affiliate.from_payload(studio) for studio in data.get("studios", [])],
            genres=[Affiliate.from_payload(genre) for genre in data.get("genres", [])],
            explicit_genres=[Affiliate.from_payload(genre) for genre in data.get("explicit_genres", [])],
            themes=[Affiliate.from_payload(theme) for theme in data.get("themes", [])],
            demographic=[Affiliate.from_payload(demographic) for demographic in data.get("demographics", [])],
        )
