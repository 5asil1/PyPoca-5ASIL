# -*- coding: utf-8 -*-
from discord import Activity, ActivityType, Guild
from discord.ext.commands import Bot, Cog
from dislash import CommandOnCooldown, SlashInteraction

from pypoca import log
from pypoca.config import Config
from pypoca.embeds import Color, Poster
from pypoca.exceptions import NotFound
from pypoca.languages import EventReply

__all__ = ("Event", "setup")


class Event(Cog):
    """`Event` cog handles the different types of events listened by Client."""

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
    async def on_guild_join(self, guild: Guild) -> None:
        """Called when a Guild is either created by the Client or when the Client joins a guild."""

    @Cog.listener()
    async def on_slash_command_error(self, inter: SlashInteraction, e: Exception) -> None:
        """Called when a slash command fails due to some error."""
        if isinstance(e, CommandOnCooldown):
            title = (EventReply.cooldown.title.format(command_name=inter.data.name),)
            description = (EventReply.cooldown.title.format(command_name=e.retry_after),)
        elif isinstance(e, NotFound):
            title = EventReply.not_found.title
            description = EventReply.not_found.description
        else:
            title = EventReply.exception.title.format(command_name=inter.data.name)
            description = EventReply.exception.description.format(error=str(e))
            log.error(
                f"{inter}. {e}",
                extra={"locals": locals(), "ctx": vars(inter)},
                exc_info=e,
            )
        embed = Poster(title=title, description=description, color=Color.error)
        await inter.reply(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    """Setup `Event` cog."""
    bot.add_cog(Event(bot))
