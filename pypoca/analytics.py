# -*- coding: utf-8 -*-
import asyncio
from aiohttp import ClientSession
from discord import Embed, Message
from dislash import SlashInteraction
from typing import Union

from pypoca.config import DashbotConfig

__all__ = ("received", "sent")


async def _request(type: str, *, user_id: str, text: str, **kwargs) -> None:
    """Request to track conversation events on Dashbot."""
    url = "https://tracker.dashbot.io/track"
    params = {
        "v": "11.1.0-rest",
        "platform": "universal",
        "type": type,
        "apiKey": DashbotConfig.key,
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


def received(ctx: Union[Message, SlashInteraction], text: str) -> None:
    """When the bot receives a message."""
    asyncio.create_task(
        _request(
            "incoming",
            text=text,
            locale=ctx.guild.id,
            user_id=ctx.author.id,
            user_name=str(ctx.author),
        )
    )


def sent(ctx: Union[Message, SlashInteraction], text: str, embed: Embed) -> None:
    """When the bot sends a message."""
    asyncio.create_task(
        _request(
            "outgoing",
            text=text,
            locale=ctx.guild.id,
            user_id=ctx.author.id,
            user_name=str(ctx.author),
            embed=embed.to_dict(),
        )
    )
