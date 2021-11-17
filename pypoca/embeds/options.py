# -*- coding: utf-8 -*-
from dislash import Option as OptionClass
from dislash import OptionType

from pypoca.embeds.choices import Choices
from pypoca.languages import Option as OptionObject

__all__ = "Option"


class Option:
    """All valid options for slash commands."""

    language = OptionClass(
        OptionObject.language.title,
        OptionObject.language.description,
        OptionType.STRING,
        choices=Choices.languages,
    )
    region = OptionClass(
        OptionObject.region.title,
        OptionObject.region.description,
        OptionType.STRING,
        choices=Choices.regions,
    )
    hide = OptionClass(
        OptionObject.hide.title, OptionObject.hide.description, OptionType.STRING, choices=Choices.boolean
    )
    query = OptionClass(
        OptionObject.query.title,
        OptionObject.query.description,
        OptionType.STRING,
        required=True,
    )
    page = OptionClass(OptionObject.page.title, OptionObject.page.description, OptionType.INTEGER)
    nsfw = OptionClass(
        OptionObject.nsfw.title, OptionObject.nsfw.description, OptionType.STRING, choices=Choices.boolean
    )
    year = OptionClass(OptionObject.year.title, OptionObject.year.description, OptionType.INTEGER)
    min_year = OptionClass(
        OptionObject.min_year.title,
        OptionObject.min_year.description,
        OptionType.INTEGER,
    )
    max_year = OptionClass(
        OptionObject.max_year.title,
        OptionObject.max_year.description,
        OptionType.INTEGER,
    )
    min_votes = OptionClass(
        OptionObject.min_votes.title,
        OptionObject.min_votes.description,
        OptionType.INTEGER,
    )
    max_votes = OptionClass(
        OptionObject.max_votes.title,
        OptionObject.max_votes.description,
        OptionType.INTEGER,
    )
    min_rating = OptionClass(
        OptionObject.min_rating.title,
        OptionObject.min_rating.description,
        OptionType.INTEGER,
    )
    max_rating = OptionClass(
        OptionObject.max_rating.title,
        OptionObject.max_rating.description,
        OptionType.INTEGER,
    )
    min_runtime = OptionClass(
        OptionObject.min_runtime.title,
        OptionObject.min_runtime.description,
        OptionType.INTEGER,
    )
    max_runtime = OptionClass(
        OptionObject.max_runtime.title,
        OptionObject.max_runtime.description,
        OptionType.INTEGER,
    )
    # sort_by
    movie_sort_by = OptionClass(
        OptionObject.sort_by.title,
        OptionObject.sort_by.description,
        OptionType.STRING,
        choices=Choices.movie_sort_by,
    )
    tv_sort_by = OptionClass(
        OptionObject.sort_by.title,
        OptionObject.sort_by.description,
        OptionType.STRING,
        choices=Choices.tv_sort_by,
    )
    # service
    movie_service = OptionClass(
        OptionObject.service.title,
        OptionObject.service.description,
        OptionType.STRING,
        choices=Choices.movie_services,
    )
    tv_service = OptionClass(
        OptionObject.service.title,
        OptionObject.service.description,
        OptionType.STRING,
        choices=Choices.tv_services,
    )
    # genre
    movie_genre = OptionClass(
        OptionObject.genre.title,
        OptionObject.genre.description,
        OptionType.STRING,
        choices=Choices.movie_genres,
    )
    tv_genre = OptionClass(
        OptionObject.genre.title,
        OptionObject.genre.description,
        OptionType.STRING,
        choices=Choices.tv_genres,
    )
    # interval
    interval = OptionClass(
        OptionObject.interval.title,
        OptionObject.interval.description,
        OptionType.STRING,
        choices=Choices.intervals,
    )
