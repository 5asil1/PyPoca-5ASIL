# -*- coding: utf-8 -*-
import os

DEBUG = bool(os.environ.get("DEBUG", False))

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = os.environ.get("BOT_PREFIX", "/")
GUILDS_ID = os.environ.get("TEST_GUILDS_ID", "")

URLS = {
    "invite": os.environ.get("BOT_INVITE_URL"),
    "vote": os.environ.get("BOT_VOTE_URL"),
    "server": os.environ.get("BOT_SERVER_URL"),
    "site": os.environ.get("BOT_SITE_URL"),
}

COLOR = os.environ.get("COLOR_PRIMARY", 0xF1CF68)

BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY")
OMDB_KEY = os.environ.get("OMDB_KEY")
TMDB_KEY = os.environ.get("TMDB_KEY")
TRAKT_CLIENT = os.environ.get("TRAKT_TV_CLIENT_ID")
TRAKT_SECRET = os.environ.get("TRAKT_TV_CLIENT_SECRET")

DB_CREDENTIALS = {
    "provider": os.environ.get("DB_PROVIDER"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("DB_NAME"),
    "filename": os.environ.get("DB_FILENAME"),
}
