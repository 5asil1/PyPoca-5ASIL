# -*- coding: utf-8 -*-
from discord import Message
from discord.ext.commands import Bot, Cog
from dislash import SlashInteraction

from pypoca import log, utils
from pypoca.dashbot import Dashbot

__all__ = ("Analytics", "setup")


class Analytics(Cog):
    """`Analytics` cog track incoming and outgoing messages."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Called when a Message is created and sent."""
        if message.author.id != self.bot.user.id:
            return None
        embed = message.embeds[0]
        Dashbot.sent(
            message=embed.title,
            guild_id=message.guild.id,
            author_id=message.author.id,
            author_name=str(message.author),
            embed=embed.to_dict(),
        )

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Called when a Message receives an update event."""
        if after.author.id != self.bot.user.id:
            return None
        embed = after.embeds[0]
        if embed.title == before.embeds[0].title:
            return None
        Dashbot.sent(
            message=embed.title,
            guild_id=after.guild.id,
            author_id=after.author.id,
            author_name=str(after.author),
            embed=embed.to_dict(),
        )

    @Cog.listener()
    async def on_slash_command(self, inter: SlashInteraction) -> None:
        """Called when a slash command is invoked."""
        options = utils.slash_data_option_to_str(inter.data.options)
        text = f"/{inter.data.name} {options}"
        Dashbot.received(
            message=text,
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )

    @Cog.listener()
    async def on_button_click(self, inter: SlashInteraction) -> None:
        """Called when any button is clicked."""
        text = inter.clicked_button.label
        Dashbot.received(
            message=text,
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )

    @Cog.listener()
    async def on_dropdown(self, inter: SlashInteraction) -> None:
        """Called when any menu is clicked."""
        text = " ".join([option.label for option in inter.select_menu.selected_options])
        Dashbot.received(
            message=text,
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )


def setup(bot: Bot) -> None:
    """Setup `Analytics` cog."""
    if Dashbot.api_key is None:
        log.warning("No Dashbot API key configured, couldn't track")
    else:
        bot.add_cog(Analytics(bot))
