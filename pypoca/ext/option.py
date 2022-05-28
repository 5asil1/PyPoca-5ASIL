# -*- coding: utf-8 -*-
from disnake.ext import commands

from pypoca.ext.language import DEFAULT


class Option:
    language = commands.Param(
        name=DEFAULT["OPTION_LANGUAGE_NAME"],
        description=DEFAULT["OPTION_LANGUAGE_DESC"],
    )
    region = commands.Param(
        name=DEFAULT["OPTION_REGION_NAME"],
        description=DEFAULT["OPTION_REGION_DESC"],
    )
    hide = commands.Param(
        default=0,
        name=DEFAULT["OPTION_HIDE_NAME"],
        description=DEFAULT["OPTION_HIDE_DESC"],
    )
    query = commands.Param(
        name=DEFAULT["OPTION_QUERY_NAME"],
        description=DEFAULT["OPTION_QUERY_DESC"],
    )
    page = commands.Param(
        default=1,
        name=DEFAULT["OPTION_PAGE_NAME"],
        description=DEFAULT["OPTION_PAGE_DESC"],
        min_value=1,
        max_value=50,
    )
    nsfw = commands.Param(
        default=0,
        name=DEFAULT["OPTION_NSFW_NAME"],
        description=DEFAULT["OPTION_NSFW_DESC"],
    )
    year = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_YEAR_NAME"],
        description=DEFAULT["OPTION_YEAR_DESC"],
        min_value=1800,
        max_value=2200,
    )
    min_year = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MIN_YEAR_NAME"],
        description=DEFAULT["OPTION_MIN_YEAR_DESC"],
        min_value=1800,
        max_value=2200,
    )
    max_year = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MAX_YEAR_NAME"],
        description=DEFAULT["OPTION_MAX_YEAR_DESC"],
        min_value=1800,
        max_value=2200,
    )
    min_votes = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MIN_VOTES_NAME"],
        description=DEFAULT["OPTION_MIN_VOTES_DESC"],
    )
    max_votes = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MAX_VOTES_NAME"],
        description=DEFAULT["OPTION_MAX_VOTES_DESC"],
    )
    min_rating = commands.Param(
        default=-1.0,
        name=DEFAULT["OPTION_MIN_RATING_NAME"],
        description=DEFAULT["OPTION_MIN_RATING_DESC"],
        min_value=0,
        max_value=10,
    )
    max_rating = commands.Param(
        default=-1.0,
        name=DEFAULT["OPTION_MAX_RATING_NAME"],
        description=DEFAULT["OPTION_MAX_RATING_DESC"],
        min_value=0,
        max_value=10,
    )
    min_runtime = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MIN_RUNTIME_NAME"],
        description=DEFAULT["OPTION_MIN_RUNTIME_DESC"],
    )
    max_runtime = commands.Param(
        default=-1,
        name=DEFAULT["OPTION_MAX_RUNTIME_NAME"],
        description=DEFAULT["OPTION_MAX_RUNTIME_DESC"],
    )
    movie_sort_by = commands.Param(
        default="popularity.desc",
        name=DEFAULT["OPTION_SORT_BY_NAME"],
        description=DEFAULT["OPTION_SORT_BY_DESC"],
    )
    tv_sort_by = commands.Param(
        default="popularity.desc",
        name=DEFAULT["OPTION_SORT_BY_NAME"],
        description=DEFAULT["OPTION_SORT_BY_DESC"],
    )
    movie_service = commands.Param(
        default=None,
        name=DEFAULT["OPTION_SERVICE_NAME"],
        description=DEFAULT["OPTION_SERVICE_DESC"],
    )
    tv_service = commands.Param(
        default=None,
        name=DEFAULT["OPTION_SERVICE_NAME"],
        description=DEFAULT["OPTION_SERVICE_DESC"],
    )
    movie_genre = commands.Param(
        default=None,
        name=DEFAULT["OPTION_GENRE_NAME"],
        description=DEFAULT["OPTION_GENRE_DESC"],
    )
    tv_genre = commands.Param(
        default=None,
        name=DEFAULT["OPTION_GENRE_NAME"],
        description=DEFAULT["OPTION_GENRE_DESC"],
    )
    interval = commands.Param(
        default="day",
        name=DEFAULT["OPTION_INTERVAL_NAME"],
        description=DEFAULT["OPTION_INTERVAL_DESC"],
    )
