# -*- coding: utf-8 -*-
from dislash import OptionChoice

from pypoca.languages import FALSE, TRUE, Genre, Interval, Language, Region, Sort

__all__ = ("Choice", "Choices")


class Choice:
    """All valid choice options for option."""

    # boolean
    true = OptionChoice(TRUE, True)
    false = OptionChoice(FALSE, False)
    # sort_by
    popularity = OptionChoice(Sort.popularity, "popularity.desc")
    year = OptionChoice(Sort.year, "release_date.desc")
    rating = OptionChoice(Sort.rating, "vote_average.desc")
    title = OptionChoice(Sort.title, "original_title.asc")
    votes = OptionChoice(Sort.votes, "vote_count.desc")
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
    action = OptionChoice(Genre.action, "28")
    adventure = OptionChoice(Genre.adventure, "12")
    animation = OptionChoice(Genre.animation, "16")
    comedy = OptionChoice(Genre.comedy, "35")
    crime = OptionChoice(Genre.crime, "80")
    documentary = OptionChoice(Genre.documentary, "99")
    drama = OptionChoice(Genre.drama, "18")
    family = OptionChoice(Genre.family, "10751")
    fantasy = OptionChoice(Genre.fantasy, "14")
    history = OptionChoice(Genre.history, "36")
    horror = OptionChoice(Genre.horror, "27")
    music = OptionChoice(Genre.music, "10402")
    mystery = OptionChoice(Genre.mystery, "9648")
    romance = OptionChoice(Genre.romance, "10749")
    syfy = OptionChoice(Genre.syfy, "878")
    tv = OptionChoice(Genre.tv, "10770")
    thriller = OptionChoice(Genre.thriller, "53")
    war = OptionChoice(Genre.war, "10752")
    western = OptionChoice(Genre.western, "37")
    action_and_adventure = OptionChoice(Genre.action_and_adventure, "10759")
    kids = OptionChoice(Genre.kids, "10762")
    news = OptionChoice(Genre.news, "10763")
    reality = OptionChoice(Genre.reality, "10764")
    syfy_and_fantasy = OptionChoice(Genre.syfy_and_fantasy, "10765")
    soap = OptionChoice(Genre.soap, "10766")
    talk = OptionChoice(Genre.talk, "10767")
    war_and_politics = OptionChoice(Genre.war_and_politics, "10768")
    # interval
    day = OptionChoice(Interval.day, "day")
    week = OptionChoice(Interval.week, "week")


class Choices:
    """All valid list of choice options for option."""

    languages = [OptionChoice(value, key.replace("_", "-")) for key, value in vars(Language).items() if key[0] != "_"]
    regions = [OptionChoice(value, key) for key, value in vars(Region).items() if key[0] != "_"]
    # boolean
    boolean = [Choice.true, Choice.false]
    # sort_by
    movie_sort_by = [
        Choice.popularity,
        Choice.year,
        Choice.rating,
        Choice.title,
        Choice.votes,
    ]
    tv_sort_by = [Choice.popularity, Choice.year, Choice.rating]
    # service
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
    # genre
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
    # interval
    intervals = [Choice.day, Choice.week]
