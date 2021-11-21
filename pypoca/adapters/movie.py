# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca import utils
from pypoca.languages import Field

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
    try:
        trakt_id = result["external_ids"]["trakt"]
        watch_providers = [
            f"[{watch_provider}]({utils.watch_provider_url(watch_provider, 'movie', trakt_id, region)})"
            for watch_provider in watch_providers
        ]
    except Exception:
        pass

    embed = {
        "title": result.get("title") or result.original_title,
        "description": result.get("overview"),
        "fields": [
            {"name": Field.rating, "value": rating or "-"},
            {"name": Field.released, "value": release_date or "-"},
            {"name": Field.watch, "value": ", ".join(watch_providers) if watch_providers else "-"},
            {"name": Field.runtime, "value": duration or "-"},
            {"name": Field.genre, "value": ", ".join(genres) if genres else "-"},
            {"name": Field.studios, "value": ", ".join(production_companies) if production_companies else "-"},
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
        {"label": Field.trailer, "url": f"https://www.youtube.com/watch?v={video_key}", "disabled": not video_key},
        {"label": "IMDb", "url": f"https://www.imdb.com/title/{imdb_id}", "disabled": not imdb_id},
        {"label": Field.cast, "custom_id": "cast", "disabled": not result.credits.cast},
        {"label": Field.crew, "custom_id": "crew", "disabled": not result.credits.crew},
        {"label": Field.similar, "custom_id": "similar", "disabled": not result.recommendations.results},
    ]
    return buttons
