# -*- coding: utf-8 -*-
from aiohttp import ClientSession

from pypoca.config import TRAKT_CLIENT, TRAKT_SECRET
from pypoca.exceptions import TraktException


class Trakt:
    @property
    def host(self) -> str:
        return "https://api.trakt.tv"

    @property
    def version(self) -> str:
        return "2"

    @property
    def client(self) -> str:
        return TRAKT_CLIENT

    @property
    def secret(self) -> str:
        return TRAKT_SECRET

    @property
    def default_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "trakt-api-version": self.version,
            "trakt-api-key": self.client,
        }

    async def request(self, path: str, method: str = "GET", **kwargs) -> dict:
        url = f"{self.host}/{path}"
        headers = self.default_headers

        async with ClientSession() as session:
            async with await session.request(method, url=url, headers=headers) as response:
                try:
                    response.raise_for_status()
                    result = await response.json()
                except Exception as e:
                    raise TmdbException(e)
                else:
                    return result


class Movie(Trakt):
    async def find_by_tmdb_id(self, tmdb_id: str) -> dict:
        """https://trakt.docs.apiary.io/#reference/search/id-lookup/get-id-lookup-results"""
        return await self.request(f"search/tmdb/{tmdb_id}")

    async def trakt_id_by_tmdb_id(self, tmdb_id: str) -> str:
        try:
            response = await self.find_by_tmdb_id(tmdb_id)
            return response[0]["movie"]["ids"]["trakt"]
        except Exception:
            return None


class Show(Trakt):
    async def find_by_tmdb_id(self, tmdb_id: str) -> dict:
        """https://trakt.docs.apiary.io/#reference/search/id-lookup/get-id-lookup-results"""
        return await self.request(f"search/tmdb/{tmdb_id}")

    async def trakt_id_by_tmdb_id(self, tmdb_id: str) -> str:
        try:
            response = await self.find_by_tmdb_id(tmdb_id)
            return response[0]["show"]["ids"]["trakt"]
        except Exception:
            return None
