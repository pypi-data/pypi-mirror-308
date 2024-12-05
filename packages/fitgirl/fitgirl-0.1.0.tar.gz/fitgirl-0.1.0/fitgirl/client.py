import httpx
import typing
from bs4 import BeautifulSoup
from fitgirl.core.abc import Game, GameData
from fitgirl.core.parsers import parse_game, parse_game_data


class FitGirlClient:
    def __init__(self) -> None:
        self.session = httpx.AsyncClient(base_url="https://fitgirl-repacks.site")

    async def search(self, query: str) -> typing.List[GameData]:
        resp = await self.session.get(f"?s={query}")
        soup = BeautifulSoup(resp.text, "html.parser")
        pretty_html = soup.prettify()
        return parse_game_data(pretty_html)

    async def get_game(self, game_slug: str) -> typing.List[Game]:
        resp = await self.session.get(f"{game_slug}")
        soup = BeautifulSoup(resp.text, "html.parser")
        pretty_html = soup.prettify()
        return parse_game(pretty_html)

    async def close(self):
        await self.session.aclose()
