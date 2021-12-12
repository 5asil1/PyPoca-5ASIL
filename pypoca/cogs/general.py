# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, slash_command

from pypoca.config import Config
from pypoca.embeds import Buttons, Option, Poster
from pypoca.languages import BLANK_EMOJI, Command

__all__ = ("General", "setup")


class General(Cog):
    """`General` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="ping",
        description=Command.ping.description,
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def ping(self, inter: SlashInteraction, hide: bool = False):
        """Measures latency between the bot service and the Discord client."""
        latency = int(self.bot.latency * 1000)
        embed = Poster(
            title=Command.ping.reply["title"],
            description=Command.ping.reply["description"].format(latency=latency),
        )
        await inter.reply(embed=embed, ephemeral=hide)

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="help",
        description=Command.help.description,
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def help(self, inter: SlashInteraction, hide: bool = False):
        """The implementation of the help command."""
        embed = Poster(
            title="",
            description=f"""
            **/movie**
            {BLANK_EMOJI} **discover** {Command.discover_movie.description}
            {BLANK_EMOJI} **popular** {Command.popular_movie.description}
            {BLANK_EMOJI} **search** {Command.search_movie.description}
            {BLANK_EMOJI} **top** {Command.top_movie.description}
            {BLANK_EMOJI} **trending** {Command.trending_movie.description}
            {BLANK_EMOJI} **upcoming** {Command.upcoming_movie.description}
            **/tv**
            {BLANK_EMOJI} **discover** {Command.discover_tv.description}
            {BLANK_EMOJI} **popular** {Command.popular_tv.description}
            {BLANK_EMOJI} **search** {Command.search_tv.description}
            {BLANK_EMOJI} **top** {Command.top_tv.description}
            {BLANK_EMOJI} **trending** {Command.trending_tv.description}
            {BLANK_EMOJI} **upcoming** {Command.upcoming_tv.description}
            **/people**
            {BLANK_EMOJI} **popular** {Command.popular_person.description}
            {BLANK_EMOJI} **search** {Command.search_person.description}
            {BLANK_EMOJI} **trending** {Command.trending_person.description}
            """,
        )
        buttons = Buttons(
            buttons=[
                {"label": Command.help.buttons["invite"], "url": Config.bot.invite_url},
                {"label": Command.help.buttons["vote"], "url": Config.bot.vote_url},
                {"label": Command.help.buttons["server"], "url": Config.bot.server_url},
                {"label": Command.help.buttons["github"], "url": Config.bot.github_url},
            ],
        )
        await inter.reply(embed=embed, components=[buttons], ephemeral=hide)


def setup(bot: Bot) -> None:
    """Setup `General` cog."""
    bot.add_cog(General(bot))
