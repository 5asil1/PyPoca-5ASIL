# -*- coding: utf-8 -*-
import os


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
    language = os.environ.get("BOT_LANGUAGE", "en-US")
    region = os.environ.get("BOT_REGION", "US")
    invite_url = os.environ.get("BOT_INVITE_URL")
    vote_url = os.environ.get("BOT_VOTE_URL")
    server_url = os.environ.get("BOT_SERVER_URL")
    site_url = os.environ.get("BOT_SITE_URL")


class DatabaseConfig:
    """Database configuration variables"""

    provider = os.environ.get("DB_PROVIDER")
    credentials = {
        "filename": os.environ.get("DB_FILENAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST"),
        "database": os.environ.get("DB_NAME"),
        "dns": os.environ.get("DB_DNS"),
    }


class LoggerConfig:
    """Logging configuration variables"""

    level = os.environ.get("LOG_LEVEL", "INFO")
    format = os.environ.get("LOG_FORMAT")
    filename = os.environ.get("LOG_FILE_CONFIG")


class BugsnagConfig:
    """Bugsnag configuration variables"""

    key = os.environ.get("BUGSNAG_KEY")
    level = os.environ.get("BUGSNAG_LEVEL")


class DashbotConfig:
    """Dashbot configuration variables"""

    key = os.environ.get("DASHBOT_KEY")


class TMDBConfig:
    """TMDB configuration variables"""

    key = os.environ.get("TMDB_KEY")
    debug = os.environ.get("TMDB_DEBUG")


class TraktTVConfig:
    """TraktTV configuration variables"""

    client_id = os.environ.get("TRAKT_TV_CLIENT_ID")
    client_secret = os.environ.get("TRAKT_TV_CLIENT_ID")


class Config:
    """All configuration variables"""

    debug = bool(os.environ.get("DEBUG", False))
    bot = BotConfig
    database = DatabaseConfig
    logger = LoggerConfig
    bugsnag = BugsnagConfig
    dashbot = DashbotConfig
    tmdb = TMDBConfig
    trakt_tv = TraktTVConfig
