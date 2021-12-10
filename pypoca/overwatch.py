# -*- coding: utf-8 -*-
import asyncio
import os
from pathlib import Path

from discord.ext import commands
from watchgod import Change, awatch

from pypoca import log


class Watcher:
    """The overwatch core, responsible for starting up watchers and managing cogs."""

    def __init__(
        self,
        bot: commands.Bot,
        path: str = "commands",
        loop: asyncio.BaseEventLoop = None,
    ) -> None:
        self.bot = bot
        self.path = path
        self.loop = loop

    @staticmethod
    def get_cog_name(path: str) -> str:
        """Returns the cog file name without .py appended to it."""
        return os.path.normpath(path).split(os.sep)[-1:][0][:-3]

    def get_dotted_cog_path(self, path: str) -> str:
        """Returns the full dotted path that discord.py uses to load cog files."""
        tokens = os.path.normpath(path).split(os.sep)
        root_index = list(reversed(tokens)).index(self.path.split("/")[0]) + 1
        return ".".join([token for token in tokens[-root_index:-1]])

    async def load(self, cog_dir: str) -> None:
        """Loads a cog file into the bot."""
        try:
            self.bot.load_extension(cog_dir)
        except commands.ExtensionAlreadyLoaded:
            return
        except Exception as e:
            log.exception(e)
        else:
            log.info(f"Cog created: {cog_dir}")

    async def unload(self, cog_dir: str) -> None:
        """Unloads a cog file into the bot."""
        try:
            self.bot.unload_extension(cog_dir)
        except Exception as e:
            log.exception(e)
        else:
            log.info(f"Cog deleted: {cog_dir}")

    async def reload(self, cog_dir: str) -> None:
        """Attempts to atomically reload the file into the bot."""
        try:
            self.bot.reload_extension(cog_dir)
        except Exception as e:
            log.exception(e)
        else:
            log.info(f"Cog updated: {cog_dir}")

    async def _start(self) -> None:
        """Starts a watcher, monitoring for any file changes and dispatching event-related methods appropriately."""
        try:
            async for changes in awatch(Path.cwd() / self.path):
                reverse_ordered_changes = sorted(changes, reverse=True)
                for change_type, change_path in reverse_ordered_changes:
                    filename = self.get_cog_name(change_path)
                    new_dir = self.get_dotted_cog_path(change_path)
                    cog_dir = (
                        f"{new_dir}.{filename.lower()}"
                        if new_dir
                        else f"{self.path}.{filename.lower()}"
                    )
                    if change_type == Change.deleted:
                        await self.unload(cog_dir)
                    elif change_type == Change.added:
                        await self.load(cog_dir)
                    elif change_type == Change.modified and change_type != (Change.added or Change.deleted):
                        await self.reload(cog_dir)
        except FileNotFoundError:
            pass
        else:
            await asyncio.sleep(1)

    async def start(self) -> None:
        """Checks for a user-specified event loop to start on, otherwise uses current running loop."""
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        log.info(f"Watching: {Path.cwd() / self.path}")
        self.loop.create_task(self._start())
