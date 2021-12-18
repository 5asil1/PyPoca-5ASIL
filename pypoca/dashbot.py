# -*- coding: utf-8 -*-
import aiohttp
import asyncio
from dataclasses import dataclass

__all__ = "Dashbot"


@dataclass
class Dashbot:
    """Dashbot provides easy access to bot analytics."""

    api_key: str
    url: str = "https://tracker.dashbot.io/track"
    version: str = "11.1.0-rest"
    platform: str = "universal"

    def params(self, type: str) -> dict:
        """Build query params for HTTP request."""
        return {"type": type, "v": self.version, "platform": self.platform, "apiKey": self.api_key}

    def json(self, *, text: str, id: str, name: str, locale: str, extra_json: dict = {}) -> dict:
        """Build JSON payload for HTTP request."""
        user_json = {"firstName": name, "locale": locale}
        return {"userId": id, "text": text, "platformJson": extra_json, "platformUserJson": user_json}

    async def _request(self, url: str, *, params: dict, json: dict, **kwargs) -> None:
        """Request to track conversation events on Dashbot."""
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.post(url, params=params, json=json) as response:
                return await response.json()

    def received(self, message: str, guild_id: int, author_id: int, author_name: str) -> None:
        """When the bot receives a message."""
        params = self.params(type="incoming")
        json = self.json(text=message, id=author_id, name=author_name, locale=guild_id)
        asyncio.create_task(self._request(self.url, params=params, json=json))

    def sent(self, message: str, guild_id: int, author_id: int, author_name: str, embed: dict) -> None:
        """When the bot sends a message."""
        embed = {k: v for k, v in embed.items() if v}  # remove `discord.Embed.Empty` values
        params = self.params(type="outgoing")
        json = self.json(text=message, id=author_id, name=author_name, locale=guild_id, extra_json=embed)
        asyncio.create_task(self._request(self.url, params=params, json=json))
