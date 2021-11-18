# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca import utils

__all__ = ("embed", "option", "buttons")


def embed(result: AsObj, region: str) -> dict:
    """Convert a `AsObj` movie result to a `dict` with Discord embed items."""
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    genres = [genre["name"] for genre in result.get("genres", [])]
    production_companies = [company["name"] for company in result.get("production_companies", [])]
    rating = f"{vote_average} ({vote_count} votes)" if vote_average else None
    release_date = utils.format_datetime(result.release_date) or result.get("status")
    duration = utils.format_duration(result.get("runtime"))
    try:
        watch_providers = [
            watch_provider["provider_name"]
            for watch_provider in result["watch/providers"]["results"][region]["flatrate"]
        ]
    except Exception:
        watch_providers = []

    embed = {
        "title": result.get("title") or result.original_title,
        "description": result.get("overview"),
        "fields": [
            {"name": "Rating", "value": rating or "-"},
            {"name": "Released", "value": release_date or "-"},
            {"name": "Watch on", "value": ", ".join(watch_providers) if watch_providers else "-"},
            {"name": "Runtime", "value": duration or "-"},
            {"name": "Genre", "value": ", ".join(genres) if genres else "-"},
            {"name": "Studios", "value": production_companies[0] if production_companies else "-"},
        ],
    }
    if result.get("homepage"):
        embed["url"] = result.homepage
    if result.get("backdrop_path"):
        embed["image"] = {"url": f"https://image.tmdb.org/t/p/w1280/{result.backdrop_path}"}
    for person in result.credits.get("crew", []):
        if person["job"] == "Director":
            embed["author"] = {"name": person.name}
            if person.get("profile_path"):
                embed["author"]["icon_url"] = f"https://image.tmdb.org/t/p/w185/{person.profile_path}"
            break
    return embed


def option(result: AsObj) -> dict:
    """Convert a `AsObj` movie result to a `dict` with Discord option items."""
    title = result.get("title") or result.original_title
    release_date = utils.format_datetime(result.get("release_date"))
    vote_average = result.get("vote_average")
    vote_count = result.get("vote_count")
    label = f"{title} ({release_date})" if release_date else title
    description = f"{vote_average} ({vote_count} votes)" if vote_average else ""
    option = {"label": label[:100], "description": description[:100]}
    return option


def buttons(result: AsObj) -> list:
    """Convert a `AsObj` movie result to a `dict` with Discord buttons items."""
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
