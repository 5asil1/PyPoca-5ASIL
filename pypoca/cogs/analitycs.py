# -*- coding: utf-8 -*-
import asyncio
from typing import Union

from aiohttp import ClientSession
from discord import Embed, Message
from discord.ext.commands import Bot, Cog
from dislash import SlashInteraction

from pypoca import log, utils
from pypoca.config import DashbotConfig

__all__ = ("Analytics", "Dashbot", "setup")


class Dashbot:
    """Dashbot provides easy access to bot analytics."""

    api_key = DashbotConfig.key

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
    def received(cls, ctx: Union[Message, SlashInteraction], text: str) -> None:
        """When the bot receives a message."""
        asyncio.create_task(
            cls._request(
                "incoming",
                text=text,
                locale=ctx.guild.id,
                user_id=ctx.author.id,
                user_name=str(ctx.author),
            )
        )

    @classmethod
    def sent(cls, ctx: Union[Message, SlashInteraction], text: str, embed: Embed) -> None:
        """When the bot sends a message."""
        asyncio.create_task(
            cls._request(
                "outgoing",
                text=text,
                locale=ctx.guild.id,
                user_id=ctx.author.id,
                user_name=str(ctx.author),
                embed=embed.to_dict(),
            )
        )


class Analytics(Cog):
    """`Analytics` cog track incoming and outgoing messages."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Called when a Message is created and sent."""
        if message.author.id != self.bot.user.id:
            return None
        embed = message.embeds[0]
        Dashbot.sent(ctx=message, text=embed.title, embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Called when a Message receives an update event."""
        if after.author.id != self.bot.user.id:
            return None
        embed = after.embeds[0]
        if embed.title == before.embeds[0].title:
            return None
        Dashbot.sent(ctx=after, text=embed.title, embed=embed)

    @Cog.listener()
    async def on_slash_command(self, inter: SlashInteraction) -> None:
        """Called when a slash command is invoked."""
        options = utils.slash_data_option_to_str(inter.data.options)
        text = f"/{inter.data.name} {options}"
        Dashbot.received(ctx=inter, text=text)

    @Cog.listener()
    async def on_button_click(self, inter: SlashInteraction) -> None:
        """Called when any button is clicked."""
        text = inter.clicked_button.label
        Dashbot.received(ctx=inter, text=text)

    @Cog.listener()
    async def on_dropdown(self, inter: SlashInteraction) -> None:
        """Called when any menu is clicked."""
        text = " ".join([option.label for option in inter.select_menu.selected_options])
        Dashbot.received(ctx=inter, text=text)


def setup(bot: Bot) -> None:
    """Setup `Analytics` cog."""
    if Dashbot.api_key is None:
        log.warning("No Dashbot API key configured, couldn't track")
    else:
        bot.add_cog(Analytics(bot))
