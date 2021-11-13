# -*- coding: utf-8 -*-
import os


class LoggerConfig:
    """Logging configuration variables"""
    level = os.environ.get("LOG_LEVEL")
    format = os.environ.get("LOG_FORMAT")
    filename = os.environ.get("LOG_FILE_CONFIG")


class BotConfig:
    """Bot configuration variables"""
    cogs = [
        os.path.join(os.environ.get("COG_PATH"), filename)
        for filename in os.listdir(os.environ.get("COG_PATH"))
        if not filename.startswith("_") and filename.endswith(".py")
    ]
    token = os.environ.get("DISCORD_TOKEN")
    prefix = os.environ.get("BOT_PREFIX")
    guilds_ids = list(map(int, os.environ.get("TEST_GUILDS_ID").split(",")))
    language = os.environ.get("BOT_LANGUAGE")
    invite_link = os.environ.get("BOT_INVITE_LINK")
    vote_link = os.environ.get("BOT_VOTE_LINK")
    server_link = os.environ.get("BOT_SERVER_LINK")


class TMDBConfig:
    """TMDB configuration variables"""
    key = os.environ.get("TMDB_KEY")
    language = os.environ.get("TMDB_LANGUAGE")
    region = os.environ.get("TMDB_REGION")
    debug = os.environ.get("TMDB_DEBUG")


class BugsnagConfig:
    """Bugsnag configuration variables"""
    key = os.environ.get("BUGSNAG_KEY")
    level = os.environ.get("BUGSNAG_LEVEL")
