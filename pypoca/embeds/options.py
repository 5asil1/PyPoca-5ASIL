# -*- coding: utf-8 -*-
from dislash import Option as OptionClass
from dislash import OptionType

from pypoca.embeds.choices import Choices
from pypoca.languages import Option as OptionLang

__all__ = "Option"


class Option:
    """All valid options for slash commands."""

    language = OptionClass(
        OptionLang.language.title,
        OptionLang.language.description,
        OptionType.STRING,
        choices=Choices.languages,
    )
    region = OptionClass(
        OptionLang.region.title,
        OptionLang.region.description,
        OptionType.STRING,
        choices=Choices.regions,
    )
    hide = OptionClass(OptionLang.hide.title, OptionLang.hide.description, OptionType.STRING, choices=Choices.boolean)
    query = OptionClass(
        OptionLang.query.title,
        OptionLang.query.description,
        OptionType.STRING,
        required=True,
    )
    page = OptionClass(OptionLang.page.title, OptionLang.page.description, OptionType.INTEGER)
    nsfw = OptionClass(OptionLang.nsfw.title, OptionLang.nsfw.description, OptionType.STRING, choices=Choices.boolean)
    year = OptionClass(OptionLang.year.title, OptionLang.year.description, OptionType.INTEGER)
    min_year = OptionClass(
        OptionLang.min_year.title,
        OptionLang.min_year.description,
        OptionType.INTEGER,
    )
    max_year = OptionClass(
        OptionLang.max_year.title,
        OptionLang.max_year.description,
        OptionType.INTEGER,
    )
    min_votes = OptionClass(
        OptionLang.min_votes.title,
        OptionLang.min_votes.description,
        OptionType.INTEGER,
    )
    max_votes = OptionClass(
        OptionLang.max_votes.title,
        OptionLang.max_votes.description,
        OptionType.INTEGER,
    )
    min_rating = OptionClass(
        OptionLang.min_rating.title,
        OptionLang.min_rating.description,
        OptionType.INTEGER,
    )
    max_rating = OptionClass(
        OptionLang.max_rating.title,
        OptionLang.max_rating.description,
        OptionType.INTEGER,
    )
    min_runtime = OptionClass(
        OptionLang.min_runtime.title,
        OptionLang.min_runtime.description,
        OptionType.INTEGER,
    )
    max_runtime = OptionClass(
        OptionLang.max_runtime.title,
        OptionLang.max_runtime.description,
        OptionType.INTEGER,
    )
    movie_sort_by = OptionClass(
        OptionLang.sort_by.title,
        OptionLang.sort_by.description,
        OptionType.STRING,
        choices=Choices.movie_sort_by,
    )
    tv_sort_by = OptionClass(
        OptionLang.sort_by.title,
        OptionLang.sort_by.description,
        OptionType.STRING,
        choices=Choices.tv_sort_by,
    )
    movie_service = OptionClass(
        OptionLang.service.title,
        OptionLang.service.description,
        OptionType.STRING,
        choices=Choices.movie_services,
    )
    tv_service = OptionClass(
        OptionLang.service.title,
        OptionLang.service.description,
        OptionType.STRING,
        choices=Choices.tv_services,
    )
    movie_genre = OptionClass(
        OptionLang.genre.title,
        OptionLang.genre.description,
        OptionType.STRING,
        choices=Choices.movie_genres,
    )
    tv_genre = OptionClass(
        OptionLang.genre.title,
        OptionLang.genre.description,
        OptionType.STRING,
        choices=Choices.tv_genres,
    )
    interval = OptionClass(
        OptionLang.interval.title,
        OptionLang.interval.description,
        OptionType.STRING,
        choices=Choices.intervals,
    )
