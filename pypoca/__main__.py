# -*- coding: utf-8 -*-
import os

import disnake
from disnake.ext import commands

from pypoca.config import DB_CREDENTIALS, DEBUG, GUILDS_ID, TOKEN
from pypoca.database import db


def load_extensions(bot: commands.Bot, folder: str) -> None:
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"{folder}/{filename[:-3]}".replace("/", "."))


def main() -> None:
    db_credentials = {k: v for k, v in DB_CREDENTIALS.items() if v is not None}
    test_guilds = [int(guild_id) for guild_id in GUILDS_ID.split(",")] if DEBUG else None

    db.bind(**db_credentials)
    db.generate_mapping(create_tables=True)

    bot = commands.Bot(
        activity=disnake.Activity(type=disnake.ActivityType.watching, name="/help"),
        case_insensitive=True,
        command_prefix=commands.when_mentioned,
        enable_debug_events=DEBUG,
        help_command=None,
        reload=DEBUG,
        strict_localization=True,
        sync_commands=True,
        sync_commands_debug=DEBUG,
        test_guilds=test_guilds,
    )
    # bot.i18n.load("pypoca/locale")
    load_extensions(bot, "pypoca/cogs")
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
