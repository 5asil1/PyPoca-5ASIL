# -*- coding: utf-8 -*-
from discord import Activity, ActivityType
from discord.ext.commands import Bot, Cog
from dislash import CommandOnCooldown, SlashInteraction

from pypoca import log
from pypoca.embeds import Color, ReplyEmbed
from pypoca.exceptions import NotFound
from pypoca.languages import EventReply


class Event(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """An event which is activated when the bot is ready and all commands are synced."""
        activity = Activity(type=ActivityType.watching, name="/help")
        await self.bot.change_presence(activity=activity)

    @Cog.listener()
    async def on_slash_command_error(self, inter: SlashInteraction, e: Exception) -> None:
        """Called when slash command had an exception while the command was invoked."""
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
        embed = ReplyEmbed(title=title, description=description, color=Color.error)
        await inter.reply(embed=embed, ephemeral=True)

    @Cog.listener()
    async def on_component_callback_error(self, inter: SlashInteraction, e: Exception) -> None:
        """Called when component callback had an exception while the callback was invoked."""


def setup(bot: Bot) -> None:
    """Setup `Event` cog."""
    bot.add_cog(Event(bot))
