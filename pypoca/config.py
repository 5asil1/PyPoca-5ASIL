# -*- coding: utf-8 -*-
import os

DEFAULT_LINK = "https://bot.com"


class LoggerConfig:
    """Logging configuration variables"""

    level = os.environ.get("LOG_LEVEL", "INFO")
    format = os.environ.get("LOG_FORMAT")
    filename = os.environ.get("LOG_FILE_CONFIG")


class BotConfig:
    """Bot configuration variables"""

    cogs = [
        os.path.join("pypoca/cogs", filename)
        for filename in os.listdir("pypoca/cogs")
        if not filename.startswith("_") and filename.endswith(".py")
    ]
    token = os.environ["DISCORD_TOKEN"]
    prefix = os.environ.get("BOT_PREFIX", "/")
    try:
        guilds_ids = list(map(int, os.environ.get("TEST_GUILDS_ID").split(",")))
    except AttributeError:
        guilds_ids = None
    language = os.environ.get("BOT_LANGUAGE", "pt_BR")
    invite_link = os.environ.get("BOT_INVITE_LINK", DEFAULT_LINK)
    vote_link = os.environ.get("BOT_VOTE_LINK", DEFAULT_LINK)
    server_link = os.environ.get("BOT_SERVER_LINK", DEFAULT_LINK)
    github_link = os.environ.get("BOT_GITHUB_LINK", DEFAULT_LINK)


class TMDBConfig:
    """TMDB configuration variables"""

    key = os.environ.get("TMDB_KEY")
    language = os.environ.get("TMDB_LANGUAGE", "pt-BR")
    region = os.environ.get("TMDB_REGION", "BR")
    debug = os.environ.get("TMDB_DEBUG")


class BugsnagConfig:
    """Bugsnag configuration variables"""

    key = os.environ.get("BUGSNAG_KEY")
    level = os.environ.get("BUGSNAG_LEVEL")
