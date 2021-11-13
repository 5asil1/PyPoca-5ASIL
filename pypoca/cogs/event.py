# -*- coding: utf-8 -*-
from discord import Activity, ActivityType
from discord.ext.commands import Bot, Cog


class Event(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """An event which is activated when the bot is ready and all commands are synced."""
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name="/help"))


def setup(bot: Bot) -> None:
    """Setup `Event` cog."""
    bot.add_cog(Event(bot))
