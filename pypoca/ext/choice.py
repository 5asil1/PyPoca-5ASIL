# -*- coding: utf-8 -*-
from disnake.ext import commands

from pypoca.ext.language import DEFAULT


class Choice:
    language = commands.option_enum(
        {
            DEFAULT["OPTION_LANGUAGE_CHOICE_AR"]: "ar_SA",
            DEFAULT["OPTION_LANGUAGE_CHOICE_EN_US"]: "en_US",
            DEFAULT["OPTION_LANGUAGE_CHOICE_PT_BR"]: "pt_BR",
        }
    )
    region = commands.option_enum(
        {
            DEFAULT["OPTION_REGION_CHOICE_BR"]: "BR",
            DEFAULT["OPTION_REGION_CHOICE_SA"]: "SA",
            DEFAULT["OPTION_REGION_CHOICE_US"]: "US",
        }
    )
    boolean = commands.option_enum(
        {
            DEFAULT["OPTION_TRUE"]: 1,
            DEFAULT["OPTION_FALSE"]: 0,
        }
    )
    movie_sort_by = commands.option_enum(
        {
            DEFAULT["OPTION_SORT_BY_CHOICE_POPULARITY"]: "popularity.desc",
            DEFAULT["OPTION_SORT_BY_CHOICE_YEAR"]: "release_date.desc",
            DEFAULT["OPTION_SORT_BY_CHOICE_RATING"]: "vote_average.desc",
            DEFAULT["OPTION_SORT_BY_CHOICE_NAME"]: "original_title.asc",
            DEFAULT["OPTION_SORT_BY_CHOICE_VOTES"]: "vote_count.desc",
        }
    )
    tv_sort_by = commands.option_enum(
        {
            DEFAULT["OPTION_SORT_BY_CHOICE_POPULARITY"]: "popularity.desc",
            DEFAULT["OPTION_SORT_BY_CHOICE_YEAR"]: "release_date.desc",
            DEFAULT["OPTION_SORT_BY_CHOICE_RATING"]: "vote_average.desc",
        }
    )
    movie_service = commands.option_enum(
        {
            "Acorn TV": "87",
            "Amazon Prime Video": "9|119",
            "Apple iTunes": "2",
            "Apple TV Plus": "350",
            "Claro video": "167",
            "Disney Plus": "337",
            "fuboTV": "257",
            "Funimation Now": "269",
            "Globo Play": "307",
            "Google Play Movies": "3",
            "GuideDoc": "100",
            "HBO Max": "384",
            "Hulu": "15",
            "Looke": "47",
            "Mubi": "11",
            "Netflix": "8",
            "Paramount Plus": "531",
            "Peacock": "386",
            "Star Plus": "619",
            "Telecine Play": "227",
            "VIX": "457",
        }
    )
    tv_service = commands.option_enum(
        {
            "Acorn TV": "87",
            "Amazon Prime Video": "9|119",
            "Apple iTunes": "2",
            "Apple TV Plus": "350",
            "Claro video": "167",
            "Crunchyroll": "283",
            "Curiosity Stream": "190",
            "Disney Plus": "337",
            "Fox Play": "229",
            "fuboTV": "257",
            "Funimation Now": "269",
            "Globo Play": "307",
            "Google Play Movies": "3",
            "HBO Max": "384",
            "Hulu": "15",
            "Looke": "47",
            "Netflix": "8",
            "Paramount Plus": "531",
            "Peacock": "386",
            "Star Plus": "619",
            "YouTube": "192",
        }
    )
    movie_genre = commands.option_enum(
        {
            DEFAULT["OPTION_GENRE_CHOICE_ACTION"]: "28",
            DEFAULT["OPTION_GENRE_CHOICE_ADVENTURE"]: "12",
            DEFAULT["OPTION_GENRE_CHOICE_ANIMATION"]: "16",
            DEFAULT["OPTION_GENRE_CHOICE_COMEDY"]: "35",
            DEFAULT["OPTION_GENRE_CHOICE_CRIME"]: "80",
            DEFAULT["OPTION_GENRE_CHOICE_DOCUMENTARY"]: "99",
            DEFAULT["OPTION_GENRE_CHOICE_DRAMA"]: "18",
            DEFAULT["OPTION_GENRE_CHOICE_FAMILY"]: "10751",
            DEFAULT["OPTION_GENRE_CHOICE_FANTASY"]: "14",
            DEFAULT["OPTION_GENRE_CHOICE_HISTORY"]: "36",
            DEFAULT["OPTION_GENRE_CHOICE_HORROR"]: "27",
            DEFAULT["OPTION_GENRE_CHOICE_MUSIC"]: "10402",
            DEFAULT["OPTION_GENRE_CHOICE_MYSTERY"]: "9648",
            DEFAULT["OPTION_GENRE_CHOICE_ROMANCE"]: "10749",
            DEFAULT["OPTION_GENRE_CHOICE_SYFY"]: "878",
            DEFAULT["OPTION_GENRE_CHOICE_THRILLER"]: "53",
            DEFAULT["OPTION_GENRE_CHOICE_TV"]: "10770",
            DEFAULT["OPTION_GENRE_CHOICE_WAR"]: "10752",
            DEFAULT["OPTION_GENRE_CHOICE_WESTERN"]: "37",
        }
    )
    tv_genre = commands.option_enum(
        {
            DEFAULT["OPTION_GENRE_CHOICE_ACTION_AND_ADVENTURE"]: "10759",
            DEFAULT["OPTION_GENRE_CHOICE_ANIMATION"]: "16",
            DEFAULT["OPTION_GENRE_CHOICE_COMEDY"]: "35",
            DEFAULT["OPTION_GENRE_CHOICE_CRIME"]: "80",
            DEFAULT["OPTION_GENRE_CHOICE_DOCUMENTARY"]: "99",
            DEFAULT["OPTION_GENRE_CHOICE_DRAMA"]: "18",
            DEFAULT["OPTION_GENRE_CHOICE_FAMILY"]: "10751",
            DEFAULT["OPTION_GENRE_CHOICE_KIDS"]: "10762",
            DEFAULT["OPTION_GENRE_CHOICE_MYSTERY"]: "9648",
            DEFAULT["OPTION_GENRE_CHOICE_NEWS"]: "10763",
            DEFAULT["OPTION_GENRE_CHOICE_REALITY"]: "10764",
            DEFAULT["OPTION_GENRE_CHOICE_SOAP"]: "10766",
            DEFAULT["OPTION_GENRE_CHOICE_SYFY_AND_FANTASY"]: "10765",
            DEFAULT["OPTION_GENRE_CHOICE_TALK"]: "10767",
            DEFAULT["OPTION_GENRE_CHOICE_WAR_AND_POLITICS"]: "10768",
            DEFAULT["OPTION_GENRE_CHOICE_WESTERN"]: "37",
        }
    )
    interval = commands.option_enum(
        {
            DEFAULT["OPTION_INTERVAL_CHOICE_DAY"]: "day",
            DEFAULT["OPTION_INTERVAL_CHOICE_WEEK"]: "week",
        }
    )
