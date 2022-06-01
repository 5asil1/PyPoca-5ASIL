# -*- coding: utf-8 -*-
from aiohttp import ClientSession

from pypoca.config import OMDB_KEY
from pypoca.exceptions import OMDbException


class OMDb:
    @property
    def host(self) -> str:
        return "http://www.omdbapi.com"

    @property
    def key(self) -> str:
        return OMDB_KEY

    @property
    def default_params(self) -> dict:
        return {
            "apikey": self.key,
        }

    async def request(self, path: str, method: str = "GET", **kwargs) -> dict:
        url = f"{self.host}/{path}"
        params = {**self.default_params, **kwargs}

        async with ClientSession() as session:
            async with await session.request(method, url=url, params=params) as response:
                try:
                    response.raise_for_status()
                    result = await response.json()
                except Exception as e:
                    raise OMDbException(e)
                else:
                    return result


class Movie(OMDb):
    async def find_by_imdb_id(self, imdb_id: str) -> dict:
        return await self.request("", i=imdb_id, plot="full")

    async def ratings_by_imdb_id(self, imdb_id: str) -> str:
        try:
            response = await self.find_by_imdb_id(imdb_id)
            return {"imdb_rating": float(response["imdbRating"]), "imdb_votes": int(response["imdbVotes"].replace(",", ""))}
        except Exception:
            return {"imdb_rating": None, "imdb_votes": None}


class Show(OMDb):
    async def find_by_imdb_id(self, imdb_id: str) -> dict:
        return await self.request("", i=imdb_id, plot="full")

    async def ratings_by_imdb_id(self, imdb_id: str) -> str:
        try:
            response = await self.find_by_imdb_id(imdb_id)
            return {"imdb_rating": float(response["imdbRating"]), "imdb_votes": int(response["imdbVotes"].replace(",", ""))}
        except Exception:
            return {"imdb_rating": None, "imdb_votes": None}
