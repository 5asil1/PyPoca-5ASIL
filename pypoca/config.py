# -*- coding: utf-8 -*-
import os

DEFAULT_URL = "https://bot.com"


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
    except Exception:
        guilds_ids = None
    language = os.environ.get("BOT_LANGUAGE", "en_US")
    invite_url = os.environ.get("BOT_INVITE_URL", DEFAULT_URL)
    vote_url = os.environ.get("BOT_VOTE_URL", DEFAULT_URL)
    server_url = os.environ.get("BOT_SERVER_URL", DEFAULT_URL)
    github_url = os.environ.get("BOT_GITHUB_URL", DEFAULT_URL)


class TMDBConfig:
    """TMDB configuration variables"""

    key = os.environ.get("TMDB_KEY")
    language = os.environ.get("TMDB_LANGUAGE", "en-US")
    region = os.environ.get("TMDB_REGION", "US")
    debug = os.environ.get("TMDB_DEBUG")


class BugsnagConfig:
    """Bugsnag configuration variables"""

    key = os.environ.get("BUGSNAG_KEY")
    level = os.environ.get("BUGSNAG_LEVEL")


class DashbotConfig:
    """Dashbot configuration variables"""

    key = os.environ.get("DASHBOT_KEY")


class TraktTVConfig:
    """TraktTV configuration variables"""

    client_id = os.environ.get("TRAKT_TV_CLIENT_ID")
    client_secret = os.environ.get("TRAKT_TV_CLIENT_ID")
