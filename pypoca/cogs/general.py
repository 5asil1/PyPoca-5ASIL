# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, slash_command

from pypoca.config import Config
from pypoca.embeds import BLANK_EMOJI, Buttons, Option, Poster
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("General", "setup")


class General(Cog):
    """`General` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="ping",
        description=DEFAULT_LANGUAGE.commands["ping"]["description"],
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def ping(self, inter: SlashInteraction, hide: bool = False):
        """Measures latency between the bot service and the Discord client."""
        language = self.bot.servers[inter.guild_id]["language"]
        latency = int(self.bot.latency * 1000)
        embed = Poster(
            title=Language(language).commands["ping"]["reply"]["title"],
            description=Language(language).commands["ping"]["reply"]["description"].format(latency=latency),
        )
        await inter.reply(embed=embed, ephemeral=hide)

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(
        name="help",
        description=DEFAULT_LANGUAGE.commands["help"]["description"],
        options=[Option.hide],
        connectors={Option.hide.name: "hide"},
    )
    async def help(self, inter: SlashInteraction, hide: bool = False):
        """The implementation of the help command."""
        language = self.bot.servers[inter.guild_id]["language"]
        embed = Poster(
            title="",
            description=f'''
            **/movie**
            {BLANK_EMOJI} **discover** {Language(language).commands["discover_movie"]["description"]}
            {BLANK_EMOJI} **popular** {Language(language).commands["popular_movie"]["description"]}
            {BLANK_EMOJI} **search** {Language(language).commands["search_movie"]["description"]}
            {BLANK_EMOJI} **top** {Language(language).commands["top_movie"]["description"]}
            {BLANK_EMOJI} **trending** {Language(language).commands["trending_movie"]["description"]}
            {BLANK_EMOJI} **upcoming** {Language(language).commands["upcoming_movie"]["description"]}
            **/tv**
            {BLANK_EMOJI} **discover** {Language(language).commands["discover_tv"]["description"]}
            {BLANK_EMOJI} **popular** {Language(language).commands["popular_tv"]["description"]}
            {BLANK_EMOJI} **search** {Language(language).commands["search_tv"]["description"]}
            {BLANK_EMOJI} **top** {Language(language).commands["top_tv"]["description"]}
            {BLANK_EMOJI} **trending** {Language(language).commands["trending_tv"]["description"]}
            {BLANK_EMOJI} **upcoming** {Language(language).commands["upcoming_tv"]["description"]}
            **/people**
            {BLANK_EMOJI} **popular** {Language(language).commands["popular_person"]["description"]}
            {BLANK_EMOJI} **search** {Language(language).commands["search_person"]["description"]}
            {BLANK_EMOJI} **trending** {Language(language).commands["trending_person"]["description"]}
            **/setting**
            {BLANK_EMOJI} **language** {Language(language).commands["language"]["description"]}
            ''',
        )
        buttons = Buttons(
            buttons=[
                {"label": Language(language).commands["help"]["reply"]["buttons"]["invite"], "url": Config.bot.invite_url},
                {"label": Language(language).commands["help"]["reply"]["buttons"]["vote"], "url": Config.bot.vote_url},
                {"label": Language(language).commands["help"]["reply"]["buttons"]["server"], "url": Config.bot.server_url},
                {"label": Language(language).commands["help"]["reply"]["buttons"]["site"], "url": Config.bot.site_url},
            ],
        )
        await inter.reply(embed=embed, components=[buttons], ephemeral=hide)


def setup(bot: Bot) -> None:
    """Setup `General` cog."""
    bot.add_cog(General(bot))
