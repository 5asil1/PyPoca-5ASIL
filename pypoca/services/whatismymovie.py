# -*- coding: utf-8 -*-
from aiohttp import ClientSession

from pypoca.exceptions import NoResults, WhatIsMyMovieException


class Trakt:
    @property
    def host(self) -> str:
        return "https://www.whatismymovie.com"

    async def request(self, path: str, method: str = "GET", **kwargs) -> str:
        url = f"{self.host}/{path}"
        params = kwargs

        async with ClientSession() as session:
            async with session.request(method, url=url, params=params) as response:
                try:
                    response.raise_for_status()
                    result = str(await response.read())
                except Exception as e:
                    raise WhatIsMyMovieException(e)
                else:
                    return result


class Movie(Trakt):
    async def name_by_overview(self, query: str) -> str:
        response = await self.request(f"results", text=query)
        try:
            index = response.find("item?item")
            assert index != -1
            text = response[index:index+150]
            init = text.find(">")
            end = text[init:].find("<")
            assert init != end
        except Exception:
            raise NoResults()
        else:
            return text[init + 1:init + end]
