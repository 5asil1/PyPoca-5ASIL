# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, slash_command

from pypoca.config import BotConfig
from pypoca.embeds import Option, ReplyButtons, ReplyEmbed
from pypoca.languages import CommandDescription, CommandReply


class General(Cog):
    """`General` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @cooldown(rate=1, per=3, type=BucketType.channel)
    @slash_command(name="ping", description=CommandDescription.ping, options=[Option.hide])
    async def ping(self, inter: SlashInteraction, hide: bool = False):
        """Measures latency between the bot service and the Discord client."""
        latency = int(self.bot.latency * 1000)
        embed = ReplyEmbed(
            title=CommandReply.ping.title,
            description=CommandReply.ping.description.format(latency=latency),
        )
        await inter.reply(embed=embed, ephemeral=hide)

    @cooldown(rate=1, per=3, type=BucketType.channel)
    @slash_command(name="help", description=CommandDescription.help, options=[Option.hide])
    async def help(self, inter: SlashInteraction, hide: bool = False):
        """The implementation of the help command."""
        embed = ReplyEmbed(
            title=CommandReply.help.title,
            description=CommandReply.help.description,
            fields=[
                {"name": "/movie", "value": CommandDescription.movie, "inline": False},
                {"name": "/tv", "value": CommandDescription.tv, "inline": False},
                {"name": "/people", "value": CommandDescription.person, "inline": False},
            ],
        )
        buttons = ReplyButtons(
            buttons=[
                {"label": "Invite", "url": BotConfig.invite_link},
                {"label": "Vote", "url": BotConfig.vote_link},
                {"label": "Server", "url": BotConfig.server_link},
                {"label": "Github", "url": BotConfig.github_link},
            ],
        )
        await inter.reply(embed=embed, components=[buttons], ephemeral=hide)


def setup(bot: Bot) -> None:
    """Setup `General` cog."""
    bot.add_cog(General(bot))
