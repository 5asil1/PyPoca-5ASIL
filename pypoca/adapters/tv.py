# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca import utils

__all__ = ("embed", "option", "buttons")


def embed(result: AsObj, region: str) -> dict:
    """Convert a `AsObj` TV show result to a `dict` with Discord embed items."""
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    genres = [genre["name"] for genre in result.get("genres", [])]
    networks = [network["name"] for network in result.get("networks", [])]
    rating = f"{vote_average} ({vote_count} votes)" if vote_average else None
    status = result.get("status")
    first_air_date = utils.format_datetime(result.first_air_date)
    last_air_date = utils.format_datetime(result.last_air_date)
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

    embed = {
        "title": result.get("name") or result.original_name,
        "description": result.get("overview"),
        "fields": [
            {"name": "Rating", "value": rating or "-"},
            {"name": "Premiered", "value": first_air_date or "-"},
            {
                "name": "Status",
                "value": f"{status} ({last_air_date})" if status == "Ended" else status if status else "-",
            },
            {"name": "Episodes", "value": number_of_episodes or "-"},
            {"name": "Seasons", "value": number_of_seasons or "-"},
            {"name": "Runtime", "value": f"{duration} ({total_duration} total)"},
            {"name": "Genre", "value": ", ".join(genres) if genres else "-"},
            {"name": "Network", "value": networks[0] if networks else "-"},
            {"name": "Watch on", "value": ", ".join(watch_providers) if watch_providers else "-"},
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


def option(result: AsObj) -> dict:
    """Convert a `AsObj` TV show result to a `dict` with Discord option items."""
    title = result.get("name") or result.original_name
    release_date = utils.format_datetime(result.get("first_air_date"))
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    label = f"{title} ({release_date})" if release_date else title
    description = f"{vote_average} ({vote_count} votes)" if vote_average else ""
    option = {"label": label[:100], "description": description[:100]}
    return option


def buttons(result: AsObj) -> list:
    """Convert a `AsObj` TV show result to a `dict` with Discord buttons items."""
    imdb_id = result.external_ids.get("imdb_id")
    try:
        video_key = result.videos["results"][0]["key"]
    except Exception:
        video_key = None
    buttons = [
        {"label": "Trailer", "url": f"https://www.youtube.com/watch?v={video_key}", "disabled": video_key is None},
        {"label": "Watch", "url": f"https://embed.warezcdn.net/filme/{imdb_id}", "disabled": imdb_id is None},
        {"label": "IMDb", "url": f"https://www.imdb.com/title/{imdb_id}", "disabled": imdb_id is None},
        {"label": "Cast", "custom_id": "cast", "disabled": result.credits.cast == []},
        {"label": "Crew", "custom_id": "crew", "disabled": result.credits.crew == []},
    ]
    return buttons
