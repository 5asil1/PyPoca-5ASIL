# -*- coding: utf-8 -*-
from dislash import OptionChoice

from pypoca.languages import DEFAULT_LANGUAGE

__all__ = ("Choice", "Choices")


class Choice:
    """All valid choice options for option."""

    # boolean
    true = OptionChoice(DEFAULT_LANGUAGE.true, True)
    false = OptionChoice(DEFAULT_LANGUAGE.false, False)
    # language
    en_US = OptionChoice(DEFAULT_LANGUAGE.options["language"]["choices"]["en_US"], "en-US")
    pt_BR = OptionChoice(DEFAULT_LANGUAGE.options["language"]["choices"]["pt_BR"], "pt-BR")
    # region
    US = OptionChoice(DEFAULT_LANGUAGE.options["region"]["choices"]["US"], "US")
    BR = OptionChoice(DEFAULT_LANGUAGE.options["region"]["choices"]["BR"], "BR")
    # sort_by
    popularity = OptionChoice(DEFAULT_LANGUAGE.options["sort_by"]["choices"]["popularity"], "popularity.desc")
    year = OptionChoice(DEFAULT_LANGUAGE.options["sort_by"]["choices"]["year"], "release_date.desc")
    rating = OptionChoice(DEFAULT_LANGUAGE.options["sort_by"]["choices"]["rating"], "vote_average.desc")
    title = OptionChoice(DEFAULT_LANGUAGE.options["sort_by"]["choices"]["title"], "original_title.asc")
    votes = OptionChoice(DEFAULT_LANGUAGE.options["sort_by"]["choices"]["votes"], "vote_count.desc")
    # service
    acorn_tv = OptionChoice("Acorn TV", "87")
    amazon_prime_video = OptionChoice("Amazon Prime Video", "9|119")
    apple_itunes = OptionChoice("Apple iTunes", "2")
    apple_tv_plus = OptionChoice("Apple TV Plus", "350")
    claro_video = OptionChoice("Claro video", "167")
    crunchyroll = OptionChoice("Crunchyroll", "283")
    curiosity_stream = OptionChoice("Curiosity Stream", "190")
    disney_plus = OptionChoice("Disney Plus", "337")
    fox_play = OptionChoice("Fox Play", "229")
    fubo_tv = OptionChoice("fuboTV", "257")
    funimation_now = OptionChoice("Funimation Now", "269")
    globo_play = OptionChoice("Globo Play", "307")
    google_play_movies = OptionChoice("Google Play Movies", "3")
    guidedoc = OptionChoice("GuideDoc", "100")
    hbo_max = OptionChoice("HBO Max", "384")
    hulu = OptionChoice("Hulu", "15")
    looke = OptionChoice("Looke", "47")
    mubi = OptionChoice("Mubi", "11")
    netflix = OptionChoice("Netflix", "8")
    paramount_plus = OptionChoice("Paramount Plus", "531")
    peacock = OptionChoice("Peacock", "386")
    star_plus = OptionChoice("Star Plus", "619")
    telecine_play = OptionChoice("Telecine Play", "227")
    vix = OptionChoice("VIX", "457")
    youtube = OptionChoice("YouTube", "192")
    # genre
    action = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["action"], "28")
    adventure = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["adventure"], "12")
    animation = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["animation"], "16")
    comedy = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["comedy"], "35")
    crime = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["crime"], "80")
    documentary = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["documentary"], "99")
    drama = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["drama"], "18")
    family = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["family"], "10751")
    fantasy = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["fantasy"], "14")
    history = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["history"], "36")
    horror = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["horror"], "27")
    music = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["music"], "10402")
    mystery = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["mystery"], "9648")
    romance = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["romance"], "10749")
    syfy = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["syfy"], "878")
    tv = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["tv"], "10770")
    thriller = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["thriller"], "53")
    war = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["war"], "10752")
    western = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["western"], "37")
    action_and_adventure = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["action_and_adventure"], "10759")
    kids = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["kids"], "10762")
    news = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["news"], "10763")
    reality = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["reality"], "10764")
    syfy_and_fantasy = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["syfy_and_fantasy"], "10765")
    soap = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["soap"], "10766")
    talk = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["talk"], "10767")
    war_and_politics = OptionChoice(DEFAULT_LANGUAGE.options["genre"]["choices"]["war_and_politics"], "10768")
    # interval
    day = OptionChoice(DEFAULT_LANGUAGE.options["interval"]["choices"]["day"], "day")
    week = OptionChoice(DEFAULT_LANGUAGE.options["interval"]["choices"]["week"], "week")


class Choices:
    """All valid list of choice options for option."""

    languages = [Choice.pt_BR, Choice.en_US]
    regions = [Choice.BR, Choice.US]
    boolean = [Choice.true, Choice.false]
    movie_sort_by = [
        Choice.popularity,
        Choice.year,
        Choice.rating,
        Choice.title,
        Choice.votes,
    ]
    tv_sort_by = [Choice.popularity, Choice.year, Choice.rating]
    movie_services = [
        Choice.acorn_tv,
        Choice.amazon_prime_video,
        Choice.apple_itunes,
        Choice.apple_tv_plus,
        Choice.claro_video,
        Choice.disney_plus,
        Choice.fubo_tv,
        Choice.funimation_now,
        Choice.globo_play,
        Choice.google_play_movies,
        Choice.guidedoc,
        Choice.hbo_max,
        Choice.hulu,
        Choice.looke,
        Choice.mubi,
        Choice.netflix,
        Choice.paramount_plus,
        Choice.peacock,
        Choice.star_plus,
        Choice.telecine_play,
        Choice.vix,
    ]
    tv_services = [
        Choice.acorn_tv,
        Choice.amazon_prime_video,
        Choice.apple_itunes,
        Choice.apple_tv_plus,
        Choice.claro_video,
        Choice.crunchyroll,
        Choice.curiosity_stream,
        Choice.disney_plus,
        Choice.fox_play,
        Choice.fubo_tv,
        Choice.funimation_now,
        Choice.globo_play,
        Choice.google_play_movies,
        Choice.hbo_max,
        Choice.hulu,
        Choice.looke,
        Choice.netflix,
        Choice.paramount_plus,
        Choice.peacock,
        Choice.star_plus,
        Choice.youtube,
    ]
    movie_genres = [
        Choice.action,
        Choice.adventure,
        Choice.animation,
        Choice.comedy,
        Choice.crime,
        Choice.documentary,
        Choice.drama,
        Choice.family,
        Choice.fantasy,
        Choice.history,
        Choice.horror,
        Choice.music,
        Choice.mystery,
        Choice.romance,
        Choice.syfy,
        Choice.tv,
        Choice.thriller,
        Choice.war,
        Choice.western,
    ]
    tv_genres = [
        Choice.action_and_adventure,
        Choice.animation,
        Choice.comedy,
        Choice.crime,
        Choice.documentary,
        Choice.drama,
        Choice.family,
        Choice.kids,
        Choice.mystery,
        Choice.news,
        Choice.reality,
        Choice.syfy_and_fantasy,
        Choice.soap,
        Choice.talk,
        Choice.war_and_politics,
        Choice.western,
    ]
    intervals = [Choice.day, Choice.week]
