# -*- coding: utf-8 -*-
from disnake.ext.commands import Param, option_enum

from pypoca.languages import DEFAULT_LANGUAGE

__all__ = ("Choice", "Choices", "Option")


class Choice:
    """All valid choice options for option."""

    # boolean
    true = {DEFAULT_LANGUAGE.true: 1}
    false = {DEFAULT_LANGUAGE.false: 0}
    # language
    en_US = {DEFAULT_LANGUAGE.options["language"]["choices"]["en_US"]: "en-US"}
    pt_BR = {DEFAULT_LANGUAGE.options["language"]["choices"]["pt_BR"]: "pt-BR"}
    # region
    US = {DEFAULT_LANGUAGE.options["region"]["choices"]["US"]: "US"}
    BR = {DEFAULT_LANGUAGE.options["region"]["choices"]["BR"]: "BR"}
    # sort_by
    popularity = {DEFAULT_LANGUAGE.options["sort_by"]["choices"]["popularity"]: "popularity.desc"}
    year = {DEFAULT_LANGUAGE.options["sort_by"]["choices"]["year"]: "release_date.desc"}
    rating = {DEFAULT_LANGUAGE.options["sort_by"]["choices"]["rating"]: "vote_average.desc"}
    title = {DEFAULT_LANGUAGE.options["sort_by"]["choices"]["title"]: "original_title.asc"}
    votes = {DEFAULT_LANGUAGE.options["sort_by"]["choices"]["votes"]: "vote_count.desc"}
    # service
    acorn_tv = {"Acorn TV": "87"}
    amazon_prime_video = {"Amazon Prime Video": "9|119"}
    apple_itunes = {"Apple iTunes": "2"}
    apple_tv_plus = {"Apple TV Plus": "350"}
    claro_video = {"Claro video": "167"}
    crunchyroll = {"Crunchyroll": "283"}
    curiosity_stream = {"Curiosity Stream": "190"}
    disney_plus = {"Disney Plus": "337"}
    fox_play = {"Fox Play": "229"}
    fubo_tv = {"fuboTV": "257"}
    funimation_now = {"Funimation Now": "269"}
    globo_play = {"Globo Play": "307"}
    google_play_movies = {"Google Play Movies": "3"}
    guidedoc = {"GuideDoc": "100"}
    hbo_max = {"HBO Max": "384"}
    hulu = {"Hulu": "15"}
    looke = {"Looke": "47"}
    mubi = {"Mubi": "11"}
    netflix = {"Netflix": "8"}
    paramount_plus = {"Paramount Plus": "531"}
    peacock = {"Peacock": "386"}
    star_plus = {"Star Plus": "619"}
    telecine_play = {"Telecine Play": "227"}
    vix = {"VIX": "457"}
    youtube = {"YouTube": "192"}
    # genre
    action = {DEFAULT_LANGUAGE.options["genre"]["choices"]["action"]: "28"}
    adventure = {DEFAULT_LANGUAGE.options["genre"]["choices"]["adventure"]: "12"}
    animation = {DEFAULT_LANGUAGE.options["genre"]["choices"]["animation"]: "16"}
    comedy = {DEFAULT_LANGUAGE.options["genre"]["choices"]["comedy"]: "35"}
    crime = {DEFAULT_LANGUAGE.options["genre"]["choices"]["crime"]: "80"}
    documentary = {DEFAULT_LANGUAGE.options["genre"]["choices"]["documentary"]: "99"}
    drama = {DEFAULT_LANGUAGE.options["genre"]["choices"]["drama"]: "18"}
    family = {DEFAULT_LANGUAGE.options["genre"]["choices"]["family"]: "10751"}
    fantasy = {DEFAULT_LANGUAGE.options["genre"]["choices"]["fantasy"]: "14"}
    history = {DEFAULT_LANGUAGE.options["genre"]["choices"]["history"]: "36"}
    horror = {DEFAULT_LANGUAGE.options["genre"]["choices"]["horror"]: "27"}
    music = {DEFAULT_LANGUAGE.options["genre"]["choices"]["music"]: "10402"}
    mystery = {DEFAULT_LANGUAGE.options["genre"]["choices"]["mystery"]: "9648"}
    romance = {DEFAULT_LANGUAGE.options["genre"]["choices"]["romance"]: "10749"}
    syfy = {DEFAULT_LANGUAGE.options["genre"]["choices"]["syfy"]: "878"}
    tv = {DEFAULT_LANGUAGE.options["genre"]["choices"]["tv"]: "10770"}
    thriller = {DEFAULT_LANGUAGE.options["genre"]["choices"]["thriller"]: "53"}
    war = {DEFAULT_LANGUAGE.options["genre"]["choices"]["war"]: "10752"}
    western = {DEFAULT_LANGUAGE.options["genre"]["choices"]["western"]: "37"}
    action_and_adventure = {DEFAULT_LANGUAGE.options["genre"]["choices"]["action_and_adventure"]: "10759"}
    kids = {DEFAULT_LANGUAGE.options["genre"]["choices"]["kids"]: "10762"}
    news = {DEFAULT_LANGUAGE.options["genre"]["choices"]["news"]: "10763"}
    reality = {DEFAULT_LANGUAGE.options["genre"]["choices"]["reality"]: "10764"}
    syfy_and_fantasy = {DEFAULT_LANGUAGE.options["genre"]["choices"]["syfy_and_fantasy"]: "10765"}
    soap = {DEFAULT_LANGUAGE.options["genre"]["choices"]["soap"]: "10766"}
    talk = {DEFAULT_LANGUAGE.options["genre"]["choices"]["talk"]: "10767"}
    war_and_politics = {DEFAULT_LANGUAGE.options["genre"]["choices"]["war_and_politics"]: "10768"}
    # interval
    day = {DEFAULT_LANGUAGE.options["interval"]["choices"]["day"]: "day"}
    week = {DEFAULT_LANGUAGE.options["interval"]["choices"]["week"]: "week"}


class Choices:
    """All valid list of choice options for option."""

    language = option_enum({**Choice.pt_BR, **Choice.en_US})
    region = option_enum({**Choice.BR, **Choice.US})
    boolean = option_enum({**Choice.true, **Choice.false})
    movie_sort_by = option_enum(
        {
            **Choice.popularity,
            **Choice.year,
            **Choice.rating,
            **Choice.title,
            **Choice.votes,
        }
    )
    tv_sort_by = option_enum({**Choice.popularity, **Choice.year, **Choice.rating})
    movie_service = option_enum(
        {
            **Choice.acorn_tv,
            **Choice.amazon_prime_video,
            **Choice.apple_itunes,
            **Choice.apple_tv_plus,
            **Choice.claro_video,
            **Choice.disney_plus,
            **Choice.fubo_tv,
            **Choice.funimation_now,
            **Choice.globo_play,
            **Choice.google_play_movies,
            **Choice.guidedoc,
            **Choice.hbo_max,
            **Choice.hulu,
            **Choice.looke,
            **Choice.mubi,
            **Choice.netflix,
            **Choice.paramount_plus,
            **Choice.peacock,
            **Choice.star_plus,
            **Choice.telecine_play,
            **Choice.vix,
        }
    )
    tv_service = option_enum(
        {
            **Choice.acorn_tv,
            **Choice.amazon_prime_video,
            **Choice.apple_itunes,
            **Choice.apple_tv_plus,
            **Choice.claro_video,
            **Choice.crunchyroll,
            **Choice.curiosity_stream,
            **Choice.disney_plus,
            **Choice.fox_play,
            **Choice.fubo_tv,
            **Choice.funimation_now,
            **Choice.globo_play,
            **Choice.google_play_movies,
            **Choice.hbo_max,
            **Choice.hulu,
            **Choice.looke,
            **Choice.netflix,
            **Choice.paramount_plus,
            **Choice.peacock,
            **Choice.star_plus,
            **Choice.youtube,
        }
    )
    movie_genre = option_enum(
        {
            **Choice.action,
            **Choice.adventure,
            **Choice.animation,
            **Choice.comedy,
            **Choice.crime,
            **Choice.documentary,
            **Choice.drama,
            **Choice.family,
            **Choice.fantasy,
            **Choice.history,
            **Choice.horror,
            **Choice.music,
            **Choice.mystery,
            **Choice.romance,
            **Choice.syfy,
            **Choice.tv,
            **Choice.thriller,
            **Choice.war,
            **Choice.western,
        }
    )
    tv_genre = option_enum(
        {
            **Choice.action_and_adventure,
            **Choice.animation,
            **Choice.comedy,
            **Choice.crime,
            **Choice.documentary,
            **Choice.drama,
            **Choice.family,
            **Choice.kids,
            **Choice.mystery,
            **Choice.news,
            **Choice.reality,
            **Choice.syfy_and_fantasy,
            **Choice.soap,
            **Choice.talk,
            **Choice.war_and_politics,
            **Choice.western,
        }
    )
    interval = option_enum({**Choice.day, **Choice.week})


class Option:
    """All valid options for slash commands."""

    language = Param(
        name=DEFAULT_LANGUAGE.options["language"]["title"],
        description=DEFAULT_LANGUAGE.options["language"]["description"],
    )
    region = Param(
        name=DEFAULT_LANGUAGE.options["region"]["title"],
        description=DEFAULT_LANGUAGE.options["region"]["description"],
    )
    hide = Param(
        default=0,
        name=DEFAULT_LANGUAGE.options["hide"]["title"],
        description=DEFAULT_LANGUAGE.options["hide"]["description"],
    )
    query = Param(
        name=DEFAULT_LANGUAGE.options["query"]["title"],
        description=DEFAULT_LANGUAGE.options["query"]["description"],
    )
    page = Param(
        default=1,
        name=DEFAULT_LANGUAGE.options["page"]["title"],
        description=DEFAULT_LANGUAGE.options["page"]["description"],
        min_value=1,
        max_value=50,
    )
    nsfw = Param(
        default=0,
        name=DEFAULT_LANGUAGE.options["nsfw"]["title"],
        description=DEFAULT_LANGUAGE.options["nsfw"]["description"],
    )
    year = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["year"]["title"],
        description=DEFAULT_LANGUAGE.options["year"]["description"],
        min_value=1800,
        max_value=2200,
    )
    min_year = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["min_year"]["title"],
        description=DEFAULT_LANGUAGE.options["min_year"]["description"],
        min_value=1800,
        max_value=2200,
    )
    max_year = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["max_year"]["title"],
        description=DEFAULT_LANGUAGE.options["max_year"]["description"],
        min_value=1800,
        max_value=2200,
    )
    min_votes = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["min_votes"]["title"],
        description=DEFAULT_LANGUAGE.options["min_votes"]["description"],
    )
    max_votes = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["max_votes"]["title"],
        description=DEFAULT_LANGUAGE.options["max_votes"]["description"],
    )
    min_rating = Param(
        default=-1.0,
        name=DEFAULT_LANGUAGE.options["min_rating"]["title"],
        description=DEFAULT_LANGUAGE.options["min_rating"]["description"],
        min_value=0,
        max_value=10,
    )
    max_rating = Param(
        default=-1.0,
        name=DEFAULT_LANGUAGE.options["max_rating"]["title"],
        description=DEFAULT_LANGUAGE.options["max_rating"]["description"],
        min_value=0,
        max_value=10,
    )
    min_runtime = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["min_runtime"]["title"],
        description=DEFAULT_LANGUAGE.options["min_runtime"]["description"],
    )
    max_runtime = Param(
        default=-1,
        name=DEFAULT_LANGUAGE.options["max_runtime"]["title"],
        description=DEFAULT_LANGUAGE.options["max_runtime"]["description"],
    )
    movie_sort_by = Param(
        default="popularity.desc",
        name=DEFAULT_LANGUAGE.options["sort_by"]["title"],
        description=DEFAULT_LANGUAGE.options["sort_by"]["description"],
    )
    tv_sort_by = Param(
        default="popularity.desc",
        name=DEFAULT_LANGUAGE.options["sort_by"]["title"],
        description=DEFAULT_LANGUAGE.options["sort_by"]["description"],
    )
    movie_service = Param(
        default=None,
        name=DEFAULT_LANGUAGE.options["service"]["title"],
        description=DEFAULT_LANGUAGE.options["service"]["description"],
    )
    tv_service = Param(
        default=None,
        name=DEFAULT_LANGUAGE.options["service"]["title"],
        description=DEFAULT_LANGUAGE.options["service"]["description"],
    )
    movie_genre = Param(
        default=None,
        name=DEFAULT_LANGUAGE.options["genre"]["title"],
        description=DEFAULT_LANGUAGE.options["genre"]["description"],
    )
    tv_genre = Param(
        default=None,
        name=DEFAULT_LANGUAGE.options["genre"]["title"],
        description=DEFAULT_LANGUAGE.options["genre"]["description"],
    )
    interval = Param(
        default=None,
        name=DEFAULT_LANGUAGE.options["interval"]["title"],
        description=DEFAULT_LANGUAGE.options["interval"]["description"],
    )
