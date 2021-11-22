# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, slash_command

from pypoca.config import BotConfig
from pypoca.embeds import Option, Buttons, Poster
from pypoca.languages import Button, CommandDescription, CommandReply

__all__ = ("General", "setup")


class General(Cog):
    """`General` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="ping",
        description=CommandDescription.ping,
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def ping(self, inter: SlashInteraction, hide: bool = False):
        """Measures latency between the bot service and the Discord client."""
        latency = int(self.bot.latency * 1000)
        embed = Poster(
            title=CommandReply.ping.title,
            description=CommandReply.ping.description.format(latency=latency),
        )
        await inter.reply(embed=embed, ephemeral=hide)

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="help",
        description=CommandDescription.help,
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def help(self, inter: SlashInteraction, hide: bool = False):
        """The implementation of the help command."""
        embed = Poster(
            title=CommandReply.help.title,
            description=CommandReply.help.description,
            fields=[
                {"name": "/movie", "value": CommandDescription.movie, "inline": False},
                {"name": "/tv", "value": CommandDescription.tv, "inline": False},
                {"name": "/people", "value": CommandDescription.person, "inline": False},
            ],
        )
        buttons = Buttons(
            buttons=[
                {"label": Button.invite, "url": BotConfig.invite_url},
                {"label": Button.vote, "url": BotConfig.vote_url},
                {"label": Button.server, "url": BotConfig.server_url},
                {"label": Button.github, "url": BotConfig.github_url},
            ],
        )
        await inter.reply(embed=embed, components=[buttons], ephemeral=hide)


def setup(bot: Bot) -> None:
    """Setup `General` cog."""
    bot.add_cog(General(bot))
