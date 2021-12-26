# -*- coding: utf-8 -*-
from aiohttp import ClientSession

from pypoca.config import Config

__all__ = "get_trakt_id"


async def get_trakt_id(tmdb_id: str, type: str) -> str:
    """Get the Trakt.tv ID from the TMDb ID."""
    url = f"https://api.trakt.tv/search/tmdb/{tmdb_id}"
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": Config.trakt_tv.client_id,
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
    return data[0][type]["ids"]["trakt"]
