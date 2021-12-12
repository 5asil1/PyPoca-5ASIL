# -*- coding: utf-8 -*-
from dislash import OptionChoice

from pypoca.languages import FALSE, TRUE, Option

__all__ = ("Choice", "Choices")


class Choice:
    """All valid choice options for option."""

    # boolean
    true = OptionChoice(TRUE, True)
    false = OptionChoice(FALSE, False)
    # language
    en_US = OptionChoice(Option.language.choices["en_US"], "en_US")
    pt_BR = OptionChoice(Option.language.choices["pt_BR"], "pt_BR")
    # region
    US = OptionChoice(Option.region.choices["US"], "US")
    BR = OptionChoice(Option.region.choices["BR"], "BR")
    # sort_by
    popularity = OptionChoice(Option.sort_by.choices["popularity"], "popularity.desc")
    year = OptionChoice(Option.sort_by.choices["year"], "release_date.desc")
    rating = OptionChoice(Option.sort_by.choices["rating"], "vote_average.desc")
    title = OptionChoice(Option.sort_by.choices["title"], "original_title.asc")
    votes = OptionChoice(Option.sort_by.choices["votes"], "vote_count.desc")
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
    action = OptionChoice(Option.genre.choices["action"], "28")
    adventure = OptionChoice(Option.genre.choices["adventure"], "12")
    animation = OptionChoice(Option.genre.choices["animation"], "16")
    comedy = OptionChoice(Option.genre.choices["comedy"], "35")
    crime = OptionChoice(Option.genre.choices["crime"], "80")
    documentary = OptionChoice(Option.genre.choices["documentary"], "99")
    drama = OptionChoice(Option.genre.choices["drama"], "18")
    family = OptionChoice(Option.genre.choices["family"], "10751")
    fantasy = OptionChoice(Option.genre.choices["fantasy"], "14")
    history = OptionChoice(Option.genre.choices["history"], "36")
    horror = OptionChoice(Option.genre.choices["horror"], "27")
    music = OptionChoice(Option.genre.choices["music"], "10402")
    mystery = OptionChoice(Option.genre.choices["mystery"], "9648")
    romance = OptionChoice(Option.genre.choices["romance"], "10749")
    syfy = OptionChoice(Option.genre.choices["syfy"], "878")
    tv = OptionChoice(Option.genre.choices["tv"], "10770")
    thriller = OptionChoice(Option.genre.choices["thriller"], "53")
    war = OptionChoice(Option.genre.choices["war"], "10752")
    western = OptionChoice(Option.genre.choices["western"], "37")
    action_and_adventure = OptionChoice(Option.genre.choices["action_and_adventure"], "10759")
    kids = OptionChoice(Option.genre.choices["kids"], "10762")
    news = OptionChoice(Option.genre.choices["news"], "10763")
    reality = OptionChoice(Option.genre.choices["reality"], "10764")
    syfy_and_fantasy = OptionChoice(Option.genre.choices["syfy_and_fantasy"], "10765")
    soap = OptionChoice(Option.genre.choices["soap"], "10766")
    talk = OptionChoice(Option.genre.choices["talk"], "10767")
    war_and_politics = OptionChoice(Option.genre.choices["war_and_politics"], "10768")
    # interval
    day = OptionChoice(Option.interval.choices["day"], "day")
    week = OptionChoice(Option.interval.choices["week"], "week")


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
