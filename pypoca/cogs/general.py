# -*- coding: utf-8 -*-
from disnake import ApplicationCommandInteraction, Embed
from disnake.ext.commands import Bot, BucketType, Cog, cooldown, slash_command
from disnake.ui import Button, View

from pypoca.embeds import BLANK_EMOJI, Choices, Option
from pypoca.entities import Color
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("General", "setup")


class General(Cog):
    """`General` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(description=DEFAULT_LANGUAGE.commands["ping"]["description"])
    async def ping(self, inter: ApplicationCommandInteraction, hide: Choices.boolean = Option.hide):
        """Measures latency between the bot service and the Discord client."""
        latency = int(self.bot.latency * 1000)
        language = self.bot.servers[inter.guild_id]["language"]
        quotes = Language(language)
        title = quotes.commands["ping"]["reply"]["title"]
        description = quotes.commands["ping"]["reply"]["description"].format(latency=latency)
        embed = Embed(title=title, description=description, color=Color.bot)
        await inter.reply(embed=embed, ephemeral=hide)

    @cooldown(rate=1, per=5, type=BucketType.member)
    @slash_command(description=DEFAULT_LANGUAGE.commands["help"]["description"])
    async def help(self, inter: ApplicationCommandInteraction, hide: Choices.boolean = Option.hide):
        """The implementation of the help command."""
        language = self.bot.servers[inter.guild_id]["language"]
        quotes = Language(language)
        description = f"""
            **/movie**
            {BLANK_EMOJI} **discover** {quotes.commands["discover_movie"]["description"]}
            {BLANK_EMOJI} **popular** {quotes.commands["popular_movie"]["description"]}
            {BLANK_EMOJI} **search** {quotes.commands["search_movie"]["description"]}
            {BLANK_EMOJI} **top** {quotes.commands["top_movie"]["description"]}
            {BLANK_EMOJI} **trending** {quotes.commands["trending_movie"]["description"]}
            {BLANK_EMOJI} **upcoming** {quotes.commands["upcoming_movie"]["description"]}
            **/tv**
            {BLANK_EMOJI} **discover** {quotes.commands["discover_tv"]["description"]}
            {BLANK_EMOJI} **popular** {quotes.commands["popular_tv"]["description"]}
            {BLANK_EMOJI} **search** {quotes.commands["search_tv"]["description"]}
            {BLANK_EMOJI} **top** {quotes.commands["top_tv"]["description"]}
            {BLANK_EMOJI} **trending** {quotes.commands["trending_tv"]["description"]}
            {BLANK_EMOJI} **upcoming** {quotes.commands["upcoming_tv"]["description"]}
            **/people**
            {BLANK_EMOJI} **popular** {quotes.commands["popular_person"]["description"]}
            {BLANK_EMOJI} **search** {quotes.commands["search_person"]["description"]}
            {BLANK_EMOJI} **trending** {quotes.commands["trending_person"]["description"]}
            **/setting**
            {BLANK_EMOJI} **language** {quotes.commands["language"]["description"]}
        """
        buttons = [
            {
                "style": 5,
                "label": quotes.commands["help"]["reply"]["buttons"]["invite"],
                "url": self.bot.config.urls["invite"],
            },
            {
                "style": 5,
                "label": quotes.commands["help"]["reply"]["buttons"]["vote"],
                "url": self.bot.config.urls["vote"],
            },
            {
                "style": 5,
                "label": quotes.commands["help"]["reply"]["buttons"]["server"],
                "url": self.bot.config.urls["server"],
            },
            {
                "style": 5,
                "label": quotes.commands["help"]["reply"]["buttons"]["site"],
                "url": self.bot.config.urls["site"],
            },
        ]
        embed = Embed(description=description, color=Color.bot)
        view = View()
        [view.add_item(Button(**button)) for button in buttons]
        await inter.send(embed=embed, view=view, ephemeral=hide)


def setup(bot: Bot) -> None:
    """Setup `General` cog."""
    bot.add_cog(General(bot))
