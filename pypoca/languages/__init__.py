# -*- coding: utf-8 -*-
import yaml

from pypoca.config import Config

__all__ = (
    "DATETIME_FORMAT",
    "FALSE",
    "PLACEHOLDER",
    "TRUE",
    "Command",
    "Event",
    "Option",
)

if Config.bot.language == "en_US":
    filename = "en_US"
elif Config.bot.language == "pt_BR":
    filename = "pt_BR"
else:
    filename = "en_US"

with open(f"pypoca/languages/{filename}.yaml", "r") as stream:
    lang = yaml.safe_load(stream)

TRUE = lang["y"]
FALSE = lang["n"]
DATETIME_FORMAT = lang["datetime_format"]
PLACEHOLDER = lang["placeholder"]
BLANK_EMOJI = lang["emoji"]["black"]


class Option:
    """All available options with the respectives regionalized name."""

    class query:
        title = lang["option"]["query"]["title"]
        description = lang["option"]["query"]["description"]

    class page:
        title = lang["option"]["page"]["title"]
        description = lang["option"]["page"]["description"]

    class language:
        title = lang["option"]["language"]["title"]
        description = lang["option"]["language"]["description"]
        choices = {
            "en_US": lang["option"]["language"]["choices"]["en_US"],
            "pt_BR": lang["option"]["language"]["choices"]["pt_BR"],
        }

    class region:
        title = lang["option"]["region"]["title"]
        description = lang["option"]["region"]["description"]
        choices = {
            "BR": lang["option"]["region"]["choices"]["BR"],
            "US": lang["option"]["region"]["choices"]["US"],
        }

    class nsfw:
        title = lang["option"]["nsfw"]["title"]
        description = lang["option"]["nsfw"]["description"]

    class sort_by:
        title = lang["option"]["sort_by"]["title"]
        description = lang["option"]["sort_by"]["description"]
        choices = {
            "popularity": lang["option"]["sort_by"]["choices"]["popularity"],
            "year": lang["option"]["sort_by"]["choices"]["year"],
            "rating": lang["option"]["sort_by"]["choices"]["rating"],
            "title": lang["option"]["sort_by"]["choices"]["title"],
            "votes": lang["option"]["sort_by"]["choices"]["votes"],
        }

    class year:
        title = lang["option"]["year"]["title"]
        description = lang["option"]["year"]["description"]

    class min_year:
        title = lang["option"]["min_year"]["title"]
        description = lang["option"]["min_year"]["description"]

    class max_year:
        title = lang["option"]["max_year"]["title"]
        description = lang["option"]["max_year"]["description"]

    class min_votes:
        title = lang["option"]["min_votes"]["title"]
        description = lang["option"]["min_votes"]["description"]

    class max_votes:
        title = lang["option"]["max_votes"]["title"]
        description = lang["option"]["max_votes"]["description"]

    class min_rating:
        title = lang["option"]["min_rating"]["title"]
        description = lang["option"]["min_rating"]["description"]

    class max_rating:
        title = lang["option"]["max_rating"]["title"]
        description = lang["option"]["max_rating"]["description"]

    class min_runtime:
        title = lang["option"]["min_runtime"]["title"]
        description = lang["option"]["min_runtime"]["description"]

    class max_runtime:
        title = lang["option"]["max_runtime"]["title"]
        description = lang["option"]["max_runtime"]["description"]

    class interval:
        title = lang["option"]["interval"]["title"]
        description = lang["option"]["query"]["description"]
        choices = {
            "day": lang["option"]["interval"]["choices"]["day"],
            "week": lang["option"]["interval"]["choices"]["week"],
        }

    class hide:
        title = lang["option"]["hide"]["title"]
        description = lang["option"]["hide"]["description"]

    class service:
        title = lang["option"]["service"]["title"]
        description = lang["option"]["service"]["description"]

    class genre:
        title = lang["option"]["genre"]["title"]
        description = lang["option"]["genre"]["description"]
        choices = {
            "action": lang["option"]["genre"]["choices"]["action"],
            "action_and_adventure": lang["option"]["genre"]["choices"]["action_and_adventure"],
            "adventure": lang["option"]["genre"]["choices"]["adventure"],
            "animation": lang["option"]["genre"]["choices"]["animation"],
            "comedy": lang["option"]["genre"]["choices"]["comedy"],
            "crime": lang["option"]["genre"]["choices"]["crime"],
            "documentary": lang["option"]["genre"]["choices"]["documentary"],
            "drama": lang["option"]["genre"]["choices"]["drama"],
            "family": lang["option"]["genre"]["choices"]["family"],
            "fantasy": lang["option"]["genre"]["choices"]["fantasy"],
            "history": lang["option"]["genre"]["choices"]["history"],
            "horror": lang["option"]["genre"]["choices"]["horror"],
            "kids": lang["option"]["genre"]["choices"]["kids"],
            "music": lang["option"]["genre"]["choices"]["music"],
            "mystery": lang["option"]["genre"]["choices"]["mystery"],
            "news": lang["option"]["genre"]["choices"]["news"],
            "reality": lang["option"]["genre"]["choices"]["reality"],
            "romance": lang["option"]["genre"]["choices"]["romance"],
            "soap": lang["option"]["genre"]["choices"]["soap"],
            "syfy": lang["option"]["genre"]["choices"]["syfy"],
            "syfy_and_fantasy": lang["option"]["genre"]["choices"]["syfy_and_fantasy"],
            "talk": lang["option"]["genre"]["choices"]["talk"],
            "tv": lang["option"]["genre"]["choices"]["tv"],
            "thriller": lang["option"]["genre"]["choices"]["thriller"],
            "war": lang["option"]["genre"]["choices"]["war"],
            "war_and_politics": lang["option"]["genre"]["choices"]["war_and_politics"],
            "western": lang["option"]["genre"]["choices"]["western"],
        }


class Event:
    """All available events with the respectives regionalized name."""

    class cooldown:
        title = lang["event"]["cooldown"]["title"]
        description = lang["event"]["cooldown"]["description"]

    class not_found:
        title = lang["event"]["not_found"]["title"]
        description = lang["event"]["not_found"]["description"]

    class exception:
        title = lang["event"]["exception"]["title"]
        description = lang["event"]["exception"]["description"]


class Command:
    """All available commands with the respectives regionalized name."""

    class ping:
        description = lang["command"]["ping"]["description"]
        reply = {
            "title": lang["command"]["ping"]["reply"]["title"],
            "description": lang["command"]["ping"]["reply"]["description"],
        }

    class help:
        description = lang["command"]["help"]["description"]
        buttons = {
            "invite": lang["command"]["help"]["reply"]["buttons"]["invite"],
            "vote": lang["command"]["help"]["reply"]["buttons"]["vote"],
            "server": lang["command"]["help"]["reply"]["buttons"]["server"],
            "github": lang["command"]["help"]["reply"]["buttons"]["github"],
        }

    class movie:
        description = lang["command"]["movie"]["description"]
        reply = {
            "title": lang["command"]["movie"]["reply"]["title"],
        }
        fields = {
            "genre": lang["command"]["movie"]["reply"]["fields"]["genre"],
            "rating": lang["command"]["movie"]["reply"]["fields"]["rating"],
            "released": lang["command"]["movie"]["reply"]["fields"]["released"],
            "runtime": lang["command"]["movie"]["reply"]["fields"]["runtime"],
            "studios": lang["command"]["movie"]["reply"]["fields"]["studios"],
            "watch": lang["command"]["movie"]["reply"]["fields"]["watch"],
        }
        buttons = {
            "cast": lang["command"]["movie"]["reply"]["buttons"]["cast"],
            "crew": lang["command"]["movie"]["reply"]["buttons"]["crew"],
            "similar": lang["command"]["movie"]["reply"]["buttons"]["similar"],
            "trailer": lang["command"]["movie"]["reply"]["buttons"]["trailer"],
        }

    class person:
        description = lang["command"]["person"]["description"]
        reply = {
            "title": lang["command"]["person"]["reply"]["title"],
        }
        fields = {
            "birthday": lang["command"]["person"]["reply"]["fields"]["birthday"],
            "born": lang["command"]["person"]["reply"]["fields"]["born"],
            "deathday": lang["command"]["person"]["reply"]["fields"]["deathday"],
            "know_for": lang["command"]["person"]["reply"]["fields"]["know_for"],
        }
        buttons = {
            "acting": lang["command"]["person"]["reply"]["buttons"]["acting"],
            "jobs": lang["command"]["person"]["reply"]["buttons"]["jobs"],
        }

    class tv:
        description = lang["command"]["tv"]["description"]
        reply = {
            "title": lang["command"]["tv"]["reply"]["title"],
        }
        fields = {
            "episodes": lang["command"]["tv"]["reply"]["fields"]["episodes"],
            "genre": lang["command"]["tv"]["reply"]["fields"]["genre"],
            "network": lang["command"]["tv"]["reply"]["fields"]["network"],
            "premiered": lang["command"]["tv"]["reply"]["fields"]["premiered"],
            "rating": lang["command"]["tv"]["reply"]["fields"]["rating"],
            "runtime": lang["command"]["tv"]["reply"]["fields"]["runtime"],
            "seasons": lang["command"]["tv"]["reply"]["fields"]["seasons"],
            "studios": lang["command"]["tv"]["reply"]["fields"]["studios"],
        }
        buttons = {
            "cast": lang["command"]["tv"]["reply"]["buttons"]["cast"],
            "crew": lang["command"]["tv"]["reply"]["buttons"]["crew"],
            "similar": lang["command"]["tv"]["reply"]["buttons"]["similar"],
            "trailer": lang["command"]["tv"]["reply"]["buttons"]["trailer"],
        }

    class discover_movie:
        description = lang["command"]["discover_movie"]["description"]

    class discover_tv:
        description = lang["command"]["discover_tv"]["description"]

    class popular_movie:
        description = lang["command"]["popular_movie"]["description"]

    class popular_person:
        description = lang["command"]["popular_person"]["description"]

    class popular_tv:
        description = lang["command"]["popular_tv"]["description"]

    class search_movie:
        description = lang["command"]["search_movie"]["description"]

    class search_person:
        description = lang["command"]["search_person"]["description"]

    class search_tv:
        description = lang["command"]["search_tv"]["description"]

    class top_movie:
        description = lang["command"]["top_movie"]["description"]

    class top_tv:
        description = lang["command"]["top_tv"]["description"]

    class trending_movie:
        description = lang["command"]["trending_movie"]["description"]

    class trending_person:
        description = lang["command"]["trending_person"]["description"]

    class trending_tv:
        description = lang["command"]["trending_tv"]["description"]

    class upcoming_movie:
        description = lang["command"]["upcoming_movie"]["description"]

    class upcoming_tv:
        description = lang["command"]["upcoming_tv"]["description"]
