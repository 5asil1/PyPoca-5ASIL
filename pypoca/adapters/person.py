# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca import utils
from pypoca.languages import Field

__all__ = ("embed", "option", "buttons")


def embed(result: AsObj, region: str) -> dict:
    """Convert a `AsObj` person result to a `dict` with Discord embed items."""
    birthday = utils.format_datetime(result.get("birthday"))
    deathday = utils.format_datetime(result.get("deathday"))
    place_of_birth = result.get("place_of_birth")
    known_for_department = result.get("known_for_department")
    cast = [
        (person.get("name") or person.original_name)
        if person.media_type == "tv"
        else (person.get("title") or person.original_title)
        for person in result.combined_credits.cast
    ]
    crew = [
        (person.get("name") or person.original_name)
        if person.media_type == "tv"
        else (person.get("title") or person.original_title)
        for person in result.combined_credits.crew
    ]
    jobs = cast if known_for_department == "Acting" else crew

    embed = {
        "title": result.name,
        "description": result.get("biography"),
        "fields": [
            {"name": Field.birthday, "value": birthday or "-"},
            {"name": Field.deathday, "value": deathday or "-"},
            {"name": Field.born, "value": place_of_birth or "-"},
            {"name": Field.know_for, "value": ", ".join(jobs[:5]) if jobs else "-"},
        ],
    }
    if result.get("homepage"):
        embed["url"] = result.homepage
    if result.get("profile_path"):
        embed["thumbnail"] = {"url": f"https://image.tmdb.org/t/p/w1280/{result.profile_path}"}
    return embed


def option(result: AsObj) -> dict:
    """Convert a `AsObj` person result to a `dict` with Discord option items."""
    label = result.get("name") or result.original_name
    if "character" in result:
        description = result.character
    elif "job" in result:
        description = result.job
    else:
        jobs = [
            known_for.get("title") or known_for.original_title
            if known_for["media_type"] == "movie"
            else known_for.get("name") or known_for.get("original_name")
            for known_for in result["known_for"][:3]
        ]
        description = ", ".join(jobs)
    option = {"label": label[:100], "description": description[:100]}
    return option


def buttons(result: AsObj) -> list:
    """Convert a `AsObj` person result to a `dict` with Discord buttons items."""
    imdb_id = result.external_ids.get("imdb_id")
    instagram_id = result.external_ids.get("instagram_id")
    twitter_id = result.external_ids.get("twitter_id")
    buttons = [
        {"label": "IMDb", "url": f"https://www.imdb.com/name/{imdb_id}", "disabled": imdb_id is None},
        {"label": "Instagram", "url": f"https://www.instagram.com/{instagram_id}", "disabled": instagram_id is None},
        {"label": "Twitter", "url": f"https://www.twitter.com/{twitter_id}", "disabled": twitter_id is None},
    ]
    return buttons
