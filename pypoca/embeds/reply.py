# -*- coding: utf-8 -*-
from typing import List

from discord.embeds import Embed
from dislash import ActionRow, Button, ButtonStyle, SelectMenu

from pypoca.embeds import Color

__all__ = ("Buttons", "Menu", "Poster")


class Poster(Embed):
    """Represents a Discord embed."""

    def __init__(
        self, title: str, description: str = Embed.Empty, *, color: int = Color.bot, fields: List[dict] = [], **kwargs
    ) -> None:
        super().__init__(title=title, description=description, color=color, **kwargs)
        self.add_fields(fields)
        if "thumbnail" in kwargs:
            self.set_thumbnail(**kwargs["thumbnail"])
        if "author" in kwargs:
            self.set_author(**kwargs["author"])
        if "image" in kwargs:
            self.set_image(**kwargs["image"])
        if "footer" in kwargs:
            self.set_footer(**kwargs["footer"])

    def add_fields(self, fields: List[dict]) -> None:
        """Add multiple fields to the embed object."""
        for field in fields:
            inline = field.pop("inline", True)
            self.add_field(inline=inline, **field)


class Buttons(ActionRow):
    """Represents a Discord action row."""

    def __init__(self, *, buttons: List[dict] = [], **kwargs) -> None:
        super().__init__(**kwargs)
        self.add_buttons(buttons)

    def add_buttons(self, buttons: List[dict]) -> None:
        """Add multiple buttons to the action row object."""
        for button in buttons:
            style = button.get("style") or "link" if "url" in button else "secondary"
            button["style"] = getattr(ButtonStyle, style)
            self.components.append(Button.from_dict(button))


class Menu(SelectMenu):
    """Represents a Discord select menu."""

    def __init__(self, *, placeholder: str, options: List[dict] = [], **kwargs) -> None:
        super().__init__(placeholder=placeholder, **kwargs)
        self.add_buttons(options)

    def add_buttons(self, options: List[dict]) -> None:
        """Add multiple options to the select menu object."""
        for i, option in enumerate(options):
            self.add_option(**option, value=i)
