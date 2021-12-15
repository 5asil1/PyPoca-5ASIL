# -*- coding: utf-8 -*-
from discord import Embed
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, has_permissions, slash_command

from pypoca.embeds import Choices, Color, Option
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("Setting", "setup")


class Setting(Cog):
    """`Setting` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description=DEFAULT_LANGUAGE.commands["setting"]["description"])
    async def setting(self, inter: SlashInteraction):
        """Command that groups setting-related subcommands."""

    @cooldown(rate=1, per=5, type=BucketType.member)
    @has_permissions(administrator=True)
    @setting.sub_command(description=DEFAULT_LANGUAGE.commands["language"]["description"])
    async def language(self, inter: SlashInteraction, language: Choices.language = Option.language) -> None:
        """Subcommand to change bot language in server."""
        self.bot.servers[inter.guild_id] = {"language": language, "region": language[3:]}
        quotes = Language(language)
        title = quotes.commands["language"]["reply"]["title"]
        description = quotes.commands["language"]["reply"]["description"]
        embed = Embed(title=title, description=description, color=Color.bot)
        await inter.reply(embed=embed)


def setup(bot: Bot) -> None:
    """Setup `Setting` cog."""
    bot.add_cog(Setting(bot))
