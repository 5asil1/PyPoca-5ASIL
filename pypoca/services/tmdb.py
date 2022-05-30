# -*- coding: utf-8 -*-
import random
from aiohttp import ClientSession

from pypoca.config import TMDB_KEY
from pypoca.exceptions import TmdbException


class TMDb:
    def __init__(self, *, language: str = None, region: str = None):
        self.language = "en_US" if language is None else language
        self.region = "US" if region is None else region

    @property
    def host(self) -> str:
        return "https://api.themoviedb.org"

    @property
    def version(self) -> str:
        return "3"

    @property
    def key(self) -> str:
        return TMDB_KEY

    @property
    def default_params(self) -> dict:
        return {
            "api_key": self.key,
            "language": self.language.replace("_", "-"),
            "region": self.region,
            "watch_region": self.region,
        }

    async def request(self, path: str, method: str = "GET", **kwargs) -> dict:
        url = f"{self.host}/{self.version}/{path}"
        params = {
            k.replace("__", "."): "true" if v is True else "false" if v is False else v
            for k, v in kwargs.items()
            if v is not None
        }
        params = {**self.default_params, **params}

        async with ClientSession() as session:
            async with await session.request(method, url=url, params=params) as response:
                try:
                    response.raise_for_status()
                    result = await response.json()
                except Exception as e:
                    raise TmdbException(e)
                else:
                    return result


class Movies(TMDb):
    async def discover(
        self,
        *,
        page: int = 1,
        sort_by: str = "popularity.desc",
        certification_country: str = None,
        certification: str = None,
        certification__lte: str = None,
        certification__gte: str = None,
        include_adult: bool = None,
        include_video: bool = None,
        primary_release_year: int = None,
        primary_release_date__gte: str = None,
        primary_release_date__lte: str = None,
        release_date__gte: str = None,
        release_date__lte: str = None,
        with_release_type: int = None,
        year: int = None,
        vote_count__gte: int = None,
        vote_count__lte: int = None,
        vote_average__gte: float = None,
        vote_average__lte: float = None,
        with_cast: str = None,
        with_crew: str = None,
        with_people: str = None,
        with_companies: str = None,
        with_genres: str = None,
        without_genres: str = None,
        with_keywords: str = None,
        without_keywords: str = None,
        with_runtime__gte: int = None,
        with_runtime__lte: int = None,
        with_original_language: str = None,
        with_watch_providers: str = None,
        watch_region: str = None,
        with_watch_monetization_types: str = None,
    ) -> dict:
        """https://developers.themoviedb.org/3/discover/movie-discover"""
        return await self.request(
            "discover/movie",
            page=page,
            sort_by=sort_by,
            watch_region=watch_region,
            certification_country=certification_country,
            certification=certification,
            certification__lte=certification__lte,
            certification__gte=certification__gte,
            include_adult=include_adult,
            include_video=include_video,
            primary_release_year=primary_release_year,
            primary_release_date__gte=primary_release_date__gte,
            primary_release_date__lte=primary_release_date__lte,
            release_date__gte=release_date__gte,
            release_date__lte=release_date__lte,
            with_release_type=with_release_type,
            year=year,
            vote_count__gte=vote_count__gte,
            vote_count__lte=vote_count__lte,
            vote_average__gte=vote_average__gte,
            vote_average__lte=vote_average__lte,
            with_cast=with_cast,
            with_crew=with_crew,
            with_people=with_people,
            with_companies=with_companies,
            with_genres=with_genres,
            without_genres=without_genres,
            with_keywords=with_keywords,
            without_keywords=without_keywords,
            with_runtime__gte=with_runtime__gte,
            with_runtime__lte=with_runtime__lte,
            with_original_language=with_original_language,
            with_watch_providers=with_watch_providers,
            with_watch_monetization_types=with_watch_monetization_types,
        )

    async def genres(self) -> dict:
        """https://developers.themoviedb.org/3/genres/get-movie-list"""
        return await self.request("genre/movie/list")

    async def now_playing(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-now-playing"""
        return await self.request("movie/now_playing", page=page)

    async def popular(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-popular-movies"""
        return await self.request("movie/popular", page=page)

    async def providers(self) -> dict:
        """https://developers.themoviedb.org/3/watch-providers/get-movie-providers"""
        return await self.request("watch/providers/movie", watch_region=self.region)

    async def search(self, query: str, *, page: int = 1, include_adult: bool = False, year: int = None, primary_release_year: int = None) -> dict:
        """https://developers.themoviedb.org/3/search/search-movies"""
        return await self.request("search/movie", query=query, page=page, include_adult=include_adult, year=year, primary_release_year=primary_release_year)

    async def top_rated(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-top-rated-movies"""
        return await self.request("movie/top_rated", page=page)

    async def trending(self, *, interval: str = "day", page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/trending/get-trending"""
        return await self.request(f"trending/movie/{interval}", page=page)

    async def upcoming(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-upcoming"""
        return await self.request("movie/upcoming", page=page)

    async def randoms(self) -> dict:
        return await self.request(random.choice(["movie/popular", "movie/top_rated", "trending/movie/week"]), page=random.randint(1, 5))

    async def random(self, *, append: str = None, image_language: str = "null") -> dict:
        response = await self.randoms()
        return await Movie(id=random.choice(response["results"])["id"], language=self.language, region=self.region).details(append=append, image_language=image_language)


class Movie(TMDb):
    def __init__(self, *, id: int,  **kwargs) -> None:
        self.id = id
        super().__init__(**kwargs)

    async def details(self, *, append: str = None, image_language: str = "null") -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-details"""
        return await self.request(f"movie/{self.id}", append_to_response=append, include_image_language=image_language)

    async def alternative_titles(self, *, country: str = None) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-alternative-titles"""
        return await self.request(f"movie/{self.id}/alternative_titles", country=country)

    async def credits(self) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-credits"""
        return await self.request(f"movie/{self.id}/credits")

    async def external_ids(self) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-external-ids"""
        return await self.request(f"movie/{self.id}/external_ids")

    async def keywords(self) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-keywords"""
        return await self.request(f"movie/{self.id}/keywords")

    async def images(self, *, include_image_language: str = None) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-images"""
        return await self.request(f"movie/{self.id}/images", include_image_language=include_image_language)

    async def lists(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-lists"""
        return await self.request(f"movie/{self.id}/lists", page=page)

    async def providers(self) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-watch-providers"""
        return await self.request(f"movie/{self.id}/watch/providers")

    async def recommendations(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-recommendations"""
        return await self.request(f"movie/{self.id}/recommendations", page=page)

    async def release_dates(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-release-dates"""
        return await self.request(f"movie/{self.id}/release_dates", page=page)

    async def reviews(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-reviews"""
        return await self.request(f"movie/{self.id}/reviews", page=page)

    async def similar(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-similar-movies"""
        return await self.request(f"movie/{self.id}/similar", page=page)

    async def videos(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/movies/get-movie-videos"""
        return await self.request(f"movie/{self.id}/videos", page=page)


class People(TMDb):
    async def popular(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/people/get-popular-people"""
        return await self.request("person/popular", page=page)

    async def search(self, query: str, *, page: int = 1, include_adult: bool = False) -> dict:
        """https://developers.themoviedb.org/3/search/search-people"""
        return await self.request("search/person", query=query, page=page, include_adult=include_adult)

    async def trending(self, *, interval: str = "day", page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/trending/get-trending"""
        return await self.request(f"trending/person/{interval}", page=page)


class Person(TMDb):
    def __init__(self, *, id: int, **kwargs) -> None:
        self.id = id
        super().__init__(**kwargs)

    async def details(self, *, append: str = None, image_language: str = "null") -> dict:
        """https://developers.themoviedb.org/3/people/get-person-details"""
        return await self.request(f"person/{self.id}", append_to_response=append, include_image_language=image_language)

    async def movie_credits(self) -> dict:
        """https://developers.themoviedb.org/3/people/get-person-movie-credits"""
        return await self.request(f"person/{self.id}/movie_credits")

    async def tv_credits(self) -> dict:
        """https://developers.themoviedb.org/3/people/get-person-tv-credits"""
        return await self.request(f"person/{self.id}/tv_credits")

    async def combined_credits(self) -> dict:
        """https://developers.themoviedb.org/3/people/get-person-combined-credits"""
        return await self.request(f"person/{self.id}/combined_credits")

    async def external_ids(self) -> dict:
        """https://developers.themoviedb.org/3/people/get-person-external-ids"""
        return await self.request(f"person/{self.id}/external_ids")

    async def images(self) -> dict:
        """https://developers.themoviedb.org/3/people/get-person-images"""
        return await self.request(f"person/{self.id}/images")


class Shows(TMDb):
    async def airing_today(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-airing-today"""
        return await self.request("tv/airing_today", page=page)

    async def discover(
        self,
        *,
        page: int = 1,
        sort_by: str = "popularity.desc",
        air_date__gte: str = None,
        air_date__lte: str = None,
        first_air_date__gte: str = None,
        first_air_date__lte: str = None,
        first_air_date_year: int = None,
        timezone: str = None,
        vote_average__gte: float = None,
        vote_count__gte: int = None,
        with_genres: str = None,
        with_networks: str = None,
        without_genres: str = None,
        with_runtime__gte: int = None,
        with_runtime__lte: int = None,
        include_null_first_air_dates: bool = None,
        with_original_language: str = None,
        without_keywords: str = None,
        screened_theatrically: bool = None,
        with_companies: str = None,
        with_keywords: str = None,
        with_watch_providers: str = None,
        watch_region: str = None,
        with_watch_monetization_types: str = None,
    ) -> dict:
        """https://developers.themoviedb.org/3/discover/tv-discover"""
        return await self.request(
            "discover/tv",
            page=page,
            sort_by=sort_by,
            watch_region=watch_region,
            air_date__gte=air_date__gte,
            air_date__lte=air_date__lte,
            first_air_date__gte=first_air_date__gte,
            first_air_date__lte=first_air_date__lte,
            first_air_date_year=first_air_date_year,
            timezone=timezone,
            vote_average__gte=vote_average__gte,
            vote_count__gte=vote_count__gte,
            with_genres=with_genres,
            with_networks=with_networks,
            without_genres=without_genres,
            with_runtime__gte=with_runtime__gte,
            with_runtime__lte=with_runtime__lte,
            include_null_first_air_dates=include_null_first_air_dates,
            with_original_language=with_original_language,
            without_keywords=without_keywords,
            screened_theatrically=screened_theatrically,
            with_companies=with_companies,
            with_keywords=with_keywords,
            with_watch_providers=with_watch_providers,
            with_watch_monetization_types=with_watch_monetization_types,
        )

    async def genres(self) -> dict:
        """https://developers.themoviedb.org/3/genres/get-tv-list"""
        return await self.request("genre/tv/list")

    async def on_the_air(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-on-the-air"""
        return await self.request("tv/on_the_air", page=page)

    async def popular(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-popular-tv-shows"""
        return await self.request("tv/popular", page=page)

    async def providers(self, *, watch_region=None) -> dict:
        """https://developers.themoviedb.org/3/watch-providers/get-tv-providers"""
        return await self.request("watch/providers/tv", watch_region=watch_region)

    async def search(self, query: str, *, page: int = 1, include_adult: bool = False, first_air_date_year: int = None) -> dict:
        """https://developers.themoviedb.org/3/search/search-tv-shows"""
        return await self.request("search/tv", query=query, page=page, include_adult=include_adult, first_air_date_year=first_air_date_year)

    async def top_rated(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-top-rated-tv"""
        return await self.request("tv/top_rated", page=page)

    async def trending(self, *, interval: str = "day", page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/trending/get-trending"""
        return await self.request(f"trending/tv/{interval}", page=page)

    async def randoms(self) -> dict:
        return await self.request(random.choice(["tv/popular", "tv/top_rated", "trending/tv/week"]), page=random.randint(1, 5))

    async def random(self, *, append: str = None, image_language: str = "null") -> dict:
        response = await self.randoms()
        return await Show(id=random.choice(response["results"])["id"], language=self.language, region=self.region).details(append=append, image_language=image_language)


class Show(TMDb):
    def __init__(self, *, id: int,  **kwargs) -> None:
        self.id = id
        super().__init__(**kwargs)

    async def details(self, *, append: str = None, image_language: str = "null") -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-details"""
        return await self.request(f"tv/{self.id}", append_to_response=append, include_image_language=image_language)

    async def aggregate_credits(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-aggregate-credits"""
        return await self.request(f"tv/{self.id}/aggregate_credits")

    async def airing_today(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-airing-today"""
        return await self.request("tv/airing_today", page=page)

    async def alternative_titles(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-alternative-titles"""
        return await self.request(f"tv/{self.id}/alternative_titles")

    async def credits(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-credits"""
        return await self.request(f"tv/{self.id}/credits")

    async def episode_groups(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-episode-groups"""
        return await self.request(f"tv/{self.id}/episode_groups")

    async def external_ids(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-external-ids"""
        return await self.request(f"tv/{self.id}/external_ids")

    async def images(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-images"""
        return await self.request(f"tv/{self.id}/images")

    async def keywords(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-keywords"""
        return await self.request(f"tv/{self.id}/keywords")

    async def providers(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-watch-providers"""
        return await self.request(f"tv/{self.id}/watch/providers")

    async def recommendations(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-recommendations"""
        return await self.request(f"tv/{self.id}/recommendations", page=page)

    async def reviews(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-reviews"""
        return await self.request(f"tv/{self.id}/reviews", page=page)

    async def screened_theatrically(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-screened-theatrically"""
        return await self.request(f"tv/{self.id}/screened_theatrically")

    async def similar(self, *, page: int = 1) -> dict:
        """https://developers.themoviedb.org/3/tv/get-similar-tv-shows"""
        return await self.request(f"tv/{self.id}/similar", page=page)

    async def videos(self) -> dict:
        """https://developers.themoviedb.org/3/tv/get-tv-videos"""
        return await self.request(f"tv/{self.id}/videos")
