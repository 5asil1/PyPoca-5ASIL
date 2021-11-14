# -*- coding: utf-8 -*-
from typing import List

from discord.embeds import Embed
from dislash import ActionRow

from pypoca.embeds import Color


class ReplyEmbed(Embed):
    def __init__(self, title: str, description: str, *, fields: List[dict] = [], **kwargs) -> None:
        super().__init__(title=title, description=description, color=Color.bot, **kwargs)
        self.add_fields(fields)

    def add_fields(self, fields: List[dict]) -> None:
        """Add multiple fields to the embed object."""
        for field in fields:
            inline = field.pop("inline", False)
            self.add_field(inline=inline, **field)


class ReplyButtons(ActionRow):
    def __init__(self, *, buttons: List[dict] = [], **kwargs) -> None:
        super().__init__(**kwargs)
        self.add_buttons(buttons)

    def add_buttons(self, buttons: List[dict]) -> None:
        """Add multiple buttons to the action row object."""
        for button in buttons:
            style = button.pop("style", 5)
            self.add_button(style=style, **button)
