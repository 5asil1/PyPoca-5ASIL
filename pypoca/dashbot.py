# -*- coding: utf-8 -*-
import asyncio

from aiohttp import ClientSession

from pypoca.config import Config

__all__ = ("Dashbot")


class Dashbot:
    """Dashbot provides easy access to bot analytics."""

    api_key = Config.dashbot.key

    @staticmethod
    async def _request(type: str, *, user_id: str, text: str, **kwargs) -> None:
        """Request to track conversation events on Dashbot."""
        url = "https://tracker.dashbot.io/track"
        params = {
            "v": "11.1.0-rest",
            "platform": "universal",
            "type": type,
            "apiKey": Dashbot.api_key,
        }
        data = {
            "userId": user_id,
            "text": text,
            "platformJson": kwargs.get("embed"),
            "platformUserJson": {
                "firstName": kwargs.get("user_name"),
                "locale": kwargs.get("locale"),
            },
        }
        async with ClientSession(raise_for_status=True) as session:
            async with session.post(url, params=params, json=data) as response:
                return await response.json()

    @classmethod
    def received(cls, message: str, guild_id: int, author_id: int, author_name: str) -> None:
        """When the bot receives a message."""
        asyncio.create_task(
            cls._request(
                "incoming",
                text=message,
                locale=guild_id,
                user_id=author_id,
                user_name=author_name,
            )
        )

    @classmethod
    def sent(cls, message: str, guild_id: int, author_id: int, author_name: str, embed: dict) -> None:
        """When the bot sends a message."""
        asyncio.create_task(
            cls._request(
                "outgoing",
                text=message,
                locale=guild_id,
                user_id=author_id,
                user_name=author_name,
                embed=embed,
            )
        )
