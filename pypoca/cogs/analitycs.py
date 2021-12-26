# -*- coding: utf-8 -*-
from disnake import ApplicationCommandInteraction, Message, MessageInteraction
from disnake.ext.commands import Bot, Cog

from pypoca import log
from pypoca.dashbot import Dashbot

__all__ = ("Analytics", "setup")


class Analytics(Cog):
    """`Analytics` cog track incoming and outgoing messages."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dashbot = Dashbot(api_key=bot.config.dashbot.key)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Called when a Message is created and sent."""
        if message.author.id == self.bot.user.id:
            embed = message.embeds[0]
            self.dashbot.sent(
                message=embed.title,
                guild_id=message.guild.id,
                author_id=message.author.id,
                author_name=str(message.author),
                embed=embed.to_dict(),
            )

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Called when a Message receives an update event."""
        if after.author.id == self.bot.user.id and after.embeds[0].title != before.embeds[0].title:
            embed = after.embeds[0]
            self.dashbot.sent(
                message=embed.title,
                guild_id=after.guild.id,
                author_id=after.author.id,
                author_name=str(after.author),
                embed=embed.to_dict(),
            )

    @Cog.listener()
    async def on_slash_command(self, inter: ApplicationCommandInteraction) -> None:
        """Called when a slash command is invoked."""
        options = []
        for option in inter.data.options.values():
            if option.name and option.value:
                options.append(f"{option.name}={option.value}")
            elif option.name:
                options.append(option.name)
            if option.options:
                for opt in option.options.values():
                    options.append(f"{opt.name}={opt.value}")
        options = " ".join(options)
        self.dashbot.received(
            message=f"/{inter.data.name} {options}",
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )

    @Cog.listener()
    async def on_button_click(self, inter: MessageInteraction) -> None:
        """Called when any button is clicked."""
        self.dashbot.received(
            message=inter.clicked_button.label,
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )

    @Cog.listener()
    async def on_dropdown(self, inter: MessageInteraction) -> None:
        """Called when any menu is clicked."""
        self.dashbot.received(
            message=" ".join([option.label for option in inter.select_menu.selected_options]),
            guild_id=inter.guild.id,
            author_id=inter.author.id,
            author_name=str(inter.author),
        )


def setup(bot: Bot) -> None:
    """Setup `Analytics` cog."""
    if bot.config.dashbot.key is None:
        log.warning("No Dashbot API key configured, couldn't track")
    else:
        bot.add_cog(Analytics(bot))
