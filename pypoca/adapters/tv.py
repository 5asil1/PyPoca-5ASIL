# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca import utils
from pypoca.languages import Language

__all__ = ("embed", "option", "buttons")


def embed(result: AsObj, language: str, region: str) -> dict:
    """Convert a `AsObj` TV show result to a `dict` with Discord embed items."""
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    genres = [genre["name"] for genre in result.get("genres", [])]
    networks = [network["name"] for network in result.get("networks", [])]
    rating = f"{vote_average} ({vote_count} votes)" if vote_average else None
    status = result.get("status")
    first_air_date = utils.format_datetime(result.first_air_date, to_format=Language(language).datetime_format)
    last_air_date = utils.format_datetime(result.last_air_date, to_format=Language(language).datetime_format)
    number_of_episodes = result.get("number_of_episodes", 0)
    number_of_seasons = result.get("number_of_seasons", 0)
    episode_run_time = (
        sum(result.episode_run_time) / len(result.episode_run_time) if result.get("episode_run_time") else 0
    )
    total_duration = utils.format_duration(episode_run_time * number_of_episodes)
    duration = utils.format_duration(episode_run_time)
    try:
        watch_providers = [
            watch_provider["provider_name"]
            for watch_provider in result["watch/providers"]["results"][region]["flatrate"]
        ]
    except Exception:
        watch_providers = []
    try:
        trakt_id = result["external_ids"]["trakt"]
        watch_providers = [
            f"[{watch_provider}]({utils.watch_provider_url(watch_provider, 'show', trakt_id, region)})"
            for watch_provider in watch_providers
        ]
    except Exception:
        pass

    embed = {
        "title": result.get("name") or result.original_name,
        "description": result.get("overview"),
        "fields": [
            {"name": Language(language).commands["tv"]["reply"]["fields"]["rating"], "value": rating or "-"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["premiered"], "value": first_air_date or "-"},
            {
                "name": "Status",
                "value": f"{status} ({last_air_date})" if status == "Ended" else status if status else "-",
            },
            {"name": Language(language).commands["tv"]["reply"]["fields"]["episodes"], "value": number_of_episodes or "-"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["seasons"], "value": number_of_seasons or "-"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["runtime"], "value": f"{duration} ({total_duration} total)"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["genre"], "value": ", ".join(genres) if genres else "-"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["network"], "value": ", ".join(networks) if networks else "-"},
            {"name": Language(language).commands["tv"]["reply"]["fields"]["watch"], "value": ", ".join(watch_providers) if watch_providers else "-"},
        ],
    }
    if result.get("homepage"):
        embed["url"] = result.homepage
    if result.get("backdrop_path"):
        embed["image"] = {"url": f"https://image.tmdb.org/t/p/w1280/{result.backdrop_path}"}
    if result.get("created_by"):
        director = result.created_by[0]
        embed["author"] = {"name": director.name}
        if director.get("profile_path"):
            embed["author"]["icon_url"] = f"https://image.tmdb.org/t/p/w185/{director.profile_path}"
    return embed


def option(result: AsObj, language: str) -> dict:
    """Convert a `AsObj` TV show result to a `dict` with Discord option items."""
    title = result.get("name") or result.original_name
    release_date = utils.format_datetime(result.get("first_air_date"), to_format=Language(language).datetime_format)
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    label = f"{title} ({release_date})" if release_date else title
    description = f"{vote_average} ({vote_count} votes)" if vote_average else ""
    option = {"label": label[:100], "description": description[:100]}
    return option


def buttons(result: AsObj, language: str) -> list:
    """Convert a `AsObj` TV show result to a `dict` with Discord buttons items."""
    imdb_id = result.external_ids.get("imdb_id")
    try:
        video_key = result.videos["results"][0]["key"]
    except Exception:
        video_key = None
    buttons = [
        {
            "label": Language(language).commands["tv"]["reply"]["buttons"]["trailer"],
            "url": f"https://www.youtube.com/watch?v={video_key}",
            "disabled": not video_key,
        },
        {"label": "IMDb", "url": f"https://www.imdb.com/title/{imdb_id}", "disabled": not imdb_id},
        {"label": Language(language).commands["tv"]["reply"]["buttons"]["cast"], "custom_id": "cast", "disabled": not result.credits.cast},
        {"label": Language(language).commands["tv"]["reply"]["buttons"]["crew"], "custom_id": "crew", "disabled": not result.credits.crew},
        {
            "label": Language(language).commands["tv"]["reply"]["buttons"]["similar"],
            "custom_id": "similar",
            "disabled": not result.recommendations.results,
        },
    ]
    return buttons
