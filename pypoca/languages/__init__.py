# -*- coding: utf-8 -*-
import os
import yaml

from pypoca.config import Config

__all__ = ("DEFAULT_LANGUAGE", "LANGUAGES", "Language")


class Language:
    def __init__(self, language: str = Config.bot.language) -> None:
        path = os.path.join("pypoca/languages", language.replace("-", "_") + ".yaml")
        with open(path, "r") as stream:
            self.language = yaml.safe_load(stream)

    @property
    def true(self) -> str:
        """Regionalized 'yes'/'true' option."""
        return self.language["y"]

    @property
    def false(self) -> str:
        """Regionalized 'no'/'false' option."""
        return self.language["n"]

    @property
    def datetime_format(self) -> str:
        """Regionalized datetime format."""
        return self.language["datetime_format"]

    @property
    def placeholder(self) -> str:
        """Regionalized placeholder for option selection menu."""
        return self.language["placeholder"]

    @property
    def options(self) -> dict:
        """All available options with the respectives regionalized name."""
        return self.language["option"]

    @property
    def events(self) -> dict:
        """All available events with the respectives regionalized name."""
        return self.language["event"]

    @property
    def commands(self) -> dict:
        """All available commands with the respectives regionalized name."""
        return self.language["command"]


LANGUAGES = {}
for filename in [filename for filename in os.listdir("pypoca/languages") if filename.endswith(".yaml")]:
    language = filename[:-5].replace("_", "-")
    LANGUAGES[language] = Language(language)
DEFAULT_LANGUAGE = LANGUAGES[Config.bot.language.replace("_", "-")]
