# -*- coding: utf-8 -*-
from discord import Activity, ActivityType
from discord.ext.commands import Bot, Cog
from dislash import CommandOnCooldown, MissingPermissions, SlashInteraction

from pypoca import log
from pypoca.config import Config
from pypoca.embeds import Color, Poster
from pypoca.exceptions import NotFound
from pypoca.languages import Language

__all__ = ("Events", "setup")


class Events(Cog):
    """`Events` cog handles the different types of events listened by Client."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """Called when the client is done preparing the data received from Discord."""
        activity = Activity(type=ActivityType.watching, name="/help")
        await self.bot.change_presence(activity=activity)

        if Config.debug is True:
            from pypoca.overwatch import Watcher

            watcher = Watcher(self.bot, path="pypoca/cogs", loop=self.bot.loop)
            await watcher.start()

    @Cog.listener()
    async def on_slash_command_error(self, inter: SlashInteraction, e: Exception) -> None:
        """Called when a slash command fails due to some error."""
        language = self.bot.servers[inter.guild_id]["language"]
        if isinstance(e, CommandOnCooldown):
            title = Language(language).events["cooldown"]["title"].format(command_name=inter.data.name)
            description = Language(language).events["cooldown"]["description"].format(time=e.retry_after)
        elif isinstance(e, MissingPermissions):
            title = Language(language).events["not_allowed"]["title"]
            description = Language(language).events["not_allowed"]["description"]
        elif isinstance(e, NotFound):
            title = Language(language).events["not_found"]["title"]
            description = Language(language).events["not_found"]["description"]
        else:
            title = Language(language).events["exception"]["title"].format(command_name=inter.data.name)
            description = Language(language).events["exception"]["description"].format(error=str(e))
            log.error(
                f"{inter}. {e}",
                extra={"locals": locals(), "ctx": vars(inter)},
                exc_info=e,
            )
        embed = Poster(title=title, description=description, color=Color.error)
        await inter.reply(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    """Setup `Events` cog."""
    bot.add_cog(Events(bot))
