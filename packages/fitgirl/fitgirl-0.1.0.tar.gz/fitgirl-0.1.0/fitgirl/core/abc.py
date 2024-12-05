import dataclasses
import typing


@dataclasses.dataclass
class GameData:
    title: str
    date: str
    author: str
    category: str
    details: str
    download_links: typing.List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Game:
    title: str
    date: str
    author: str
    category: str
    genres_tags: str
    companies: str
    languages: str
    original_size: str
    repack_size: str
    download_links: typing.List[str] = dataclasses.field(default_factory=list)
    screenshots: typing.List[str] = dataclasses.field(default_factory=list)
    repack_features: typing.List[str] = dataclasses.field(default_factory=list)
