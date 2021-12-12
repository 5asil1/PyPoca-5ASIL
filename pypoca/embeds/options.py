# -*- coding: utf-8 -*-
from dislash import Option as OptionClass
from dislash import OptionType

from pypoca.embeds.choices import Choices
from pypoca.languages import DEFAULT_LANGUAGE

__all__ = "Option"


class Option:
    """All valid options for slash commands."""

    language = OptionClass(
        DEFAULT_LANGUAGE.options["language"]["title"],
        DEFAULT_LANGUAGE.options["language"]["description"],
        OptionType.STRING,
        choices=Choices.languages,
        required=True,
    )
    region = OptionClass(
        DEFAULT_LANGUAGE.options["region"]["title"],
        DEFAULT_LANGUAGE.options["region"]["description"],
        OptionType.STRING,
        choices=Choices.regions,
    )
    hide = OptionClass(
        DEFAULT_LANGUAGE.options["hide"]["title"],
        DEFAULT_LANGUAGE.options["hide"]["description"],
        OptionType.STRING,
        choices=Choices.boolean,
    )
    query = OptionClass(
        DEFAULT_LANGUAGE.options["query"]["title"],
        DEFAULT_LANGUAGE.options["query"]["description"],
        OptionType.STRING,
        required=True,
    )
    page = OptionClass(
        DEFAULT_LANGUAGE.options["page"]["title"],
        DEFAULT_LANGUAGE.options["page"]["description"],
        OptionType.INTEGER,
    )
    nsfw = OptionClass(
        DEFAULT_LANGUAGE.options["nsfw"]["title"],
        DEFAULT_LANGUAGE.options["nsfw"]["description"],
        OptionType.STRING,
        choices=Choices.boolean,
    )
    year = OptionClass(
        DEFAULT_LANGUAGE.options["year"]["title"],
        DEFAULT_LANGUAGE.options["year"]["description"],
        OptionType.INTEGER,
    )
    min_year = OptionClass(
        DEFAULT_LANGUAGE.options["min_year"]["title"],
        DEFAULT_LANGUAGE.options["min_year"]["description"],
        OptionType.INTEGER,
    )
    max_year = OptionClass(
        DEFAULT_LANGUAGE.options["max_year"]["title"],
        DEFAULT_LANGUAGE.options["max_year"]["description"],
        OptionType.INTEGER,
    )
    min_votes = OptionClass(
        DEFAULT_LANGUAGE.options["min_votes"]["title"],
        DEFAULT_LANGUAGE.options["min_votes"]["description"],
        OptionType.INTEGER,
    )
    max_votes = OptionClass(
        DEFAULT_LANGUAGE.options["max_votes"]["title"],
        DEFAULT_LANGUAGE.options["max_votes"]["description"],
        OptionType.INTEGER,
    )
    min_rating = OptionClass(
        DEFAULT_LANGUAGE.options["min_rating"]["title"],
        DEFAULT_LANGUAGE.options["min_rating"]["description"],
        OptionType.INTEGER,
    )
    max_rating = OptionClass(
        DEFAULT_LANGUAGE.options["max_rating"]["title"],
        DEFAULT_LANGUAGE.options["max_rating"]["description"],
        OptionType.INTEGER,
    )
    min_runtime = OptionClass(
        DEFAULT_LANGUAGE.options["min_runtime"]["title"],
        DEFAULT_LANGUAGE.options["min_runtime"]["description"],
        OptionType.INTEGER,
    )
    max_runtime = OptionClass(
        DEFAULT_LANGUAGE.options["max_runtime"]["title"],
        DEFAULT_LANGUAGE.options["max_runtime"]["description"],
        OptionType.INTEGER,
    )
    movie_sort_by = OptionClass(
        DEFAULT_LANGUAGE.options["sort_by"]["title"],
        DEFAULT_LANGUAGE.options["sort_by"]["description"],
        OptionType.STRING,
        choices=Choices.movie_sort_by,
    )
    tv_sort_by = OptionClass(
        DEFAULT_LANGUAGE.options["sort_by"]["title"],
        DEFAULT_LANGUAGE.options["sort_by"]["description"],
        OptionType.STRING,
        choices=Choices.tv_sort_by,
    )
    movie_service = OptionClass(
        DEFAULT_LANGUAGE.options["service"]["title"],
        DEFAULT_LANGUAGE.options["service"]["description"],
        OptionType.STRING,
        choices=Choices.movie_services,
    )
    tv_service = OptionClass(
        DEFAULT_LANGUAGE.options["service"]["title"],
        DEFAULT_LANGUAGE.options["service"]["description"],
        OptionType.STRING,
        choices=Choices.tv_services,
    )
    movie_genre = OptionClass(
        DEFAULT_LANGUAGE.options["genre"]["title"],
        DEFAULT_LANGUAGE.options["genre"]["description"],
        OptionType.STRING,
        choices=Choices.movie_genres,
    )
    tv_genre = OptionClass(
        DEFAULT_LANGUAGE.options["genre"]["title"],
        DEFAULT_LANGUAGE.options["genre"]["description"],
        OptionType.STRING,
        choices=Choices.tv_genres,
    )
    interval = OptionClass(
        DEFAULT_LANGUAGE.options["interval"]["title"],
        DEFAULT_LANGUAGE.options["interval"]["description"],
        OptionType.STRING,
        choices=Choices.intervals,
    )
