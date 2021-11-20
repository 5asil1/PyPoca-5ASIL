# -*- coding: utf-8 -*-
from discord import Activity, ActivityType, Message
from discord.ext.commands import Bot, Cog
from dislash import CommandOnCooldown, SlashInteraction

from pypoca import analytics, log, utils
from pypoca.embeds import Color, Poster
from pypoca.exceptions import NotFound
from pypoca.languages import EventReply


class Event(Cog):
    """`Event` cog handles the different types of events listened by Client."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """Called when the client is done preparing the data received from Discord."""
        activity = Activity(type=ActivityType.watching, name="/help")
        await self.bot.change_presence(activity=activity)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Called when a Message is created and sent."""
        if message.author.id != self.bot.user.id:
            return
        embed = message.embeds[0]
        analytics.sent(ctx=message, text=embed.title, embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Called when a Message receives an update event."""
        if after.author.id != self.bot.user.id:
            return
        embed = after.embeds[0]
        if embed.title == before.embeds[0].title:
            return
        analytics.sent(ctx=after, text=embed.title, embed=embed)

    @Cog.listener()
    async def on_slash_command(self, inter: SlashInteraction) -> None:
        """Called when a slash command is invoked."""
        options = utils.slash_data_option_to_str(inter.data.options)
        text = f"/{inter.data.name} {options}"
        analytics.received(ctx=inter, text=text)

    @Cog.listener()
    async def on_button_click(self, inter: SlashInteraction) -> None:
        """Called when any button is clicked."""
        text = inter.clicked_button.label
        analytics.received(ctx=inter, text=text)

    @Cog.listener()
    async def on_dropdown(self, inter: SlashInteraction) -> None:
        """Called when any menu is clicked."""
        text = " ".join([option.label for option in inter.select_menu.selected_options])
        analytics.received(ctx=inter, text=text)

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
        analytics.sent(ctx=inter, text=embed.title, embed=embed)


def setup(bot: Bot) -> None:
    """Setup `Event` cog."""
    bot.add_cog(Event(bot))
