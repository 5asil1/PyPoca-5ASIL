# -*- coding: utf-8 -*-
from discord.ext.commands import Bot, BucketType, Cog
from dislash import SlashInteraction, cooldown, has_permissions, slash_command

from pypoca.embeds import Option, Poster
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("Setting", "setup")


class Setting(Cog):
    """`Setting` cog has the basic commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="setting", description=DEFAULT_LANGUAGE.commands["setting"]["description"])
    async def setting(self, inter: SlashInteraction):
        """Command that groups setting-related subcommands."""

    @cooldown(rate=1, per=5, type=BucketType.member)
    @has_permissions(administrator=True)
    @setting.sub_command(
        name="language",
        description=DEFAULT_LANGUAGE.commands["language"]["description"],
        options=[Option.language],
        connectors={Option.language.name: "language"},
    )
    async def language(self, inter: SlashInteraction, language: str) -> None:
        """Subcommand to change bot language in server."""
        self.bot.servers[inter.guild_id] = {"language": language, "region": language[3:]}
        embed = Poster(
            title=Language(language).commands["language"]["reply"]["title"],
            description=Language(language).commands["language"]["reply"]["description"],
        )
        await inter.reply(embed=embed)


def setup(bot: Bot) -> None:
    """Setup `Setting` cog."""
    bot.add_cog(Setting(bot))
