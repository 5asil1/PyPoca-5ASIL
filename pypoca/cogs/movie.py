# -*- coding: utf-8 -*-
from typing import List

from aiotmdb import TMDB
from disnake import ApplicationCommandInteraction, Embed
from disnake.ext.commands import Bot, Cog, slash_command

from pypoca import utils
from pypoca.embeds import Choices, Menu, Option
from pypoca.entities import Color, Movie
from pypoca.exceptions import NotFound
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("Movies", "setup")


class Movies(Cog):
    """`Movies` cog has all movie related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def get_movie_by_id(movie_id: int, language: str, region: str) -> Movie:
        result = await TMDB.movie(language=language, region=region).details(
            movie_id,
            append_to_response="credits,external_ids,recommendations,videos,watch/providers",
        )
        try:
            result["external_ids"]["trakt_id"] = await utils.get_trakt_id(movie_id, type="movie")
        except Exception:
            result["external_ids"]["trakt_id"] = None
        result["id"] = movie_id
        return Movie.from_tmdb(result)

    @staticmethod
    async def _reply(
        inter: ApplicationCommandInteraction,
        *,
        results: List[dict],
        page: int,
        total_pages: int,
        language: str,
        region: str,
    ) -> None:
        if len(results) == 0:
            raise NotFound()
        quotes = Language(language)
        movies = [Movie.from_tmdb(result) for result in results]
        embed = Embed(title=quotes.commands["movie"]["reply"]["title"], color=Color.bot)
        menu = Menu(inter.bot, movies, callback=Movies.get_movie_by_id, language=language, region=region)
        await inter.send(embed=embed, view=menu)

    @slash_command(description=DEFAULT_LANGUAGE.commands["movie"]["description"])
    async def movie(self, inter: ApplicationCommandInteraction):
        """Command that groups movie-related subcommands."""

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["discover_movie"]["description"])
    async def discover(
        self,
        inter: ApplicationCommandInteraction,
        sort_by: Choices.movie_sort_by = Option.movie_sort_by,
        service: Choices.movie_service = Option.movie_service,
        genre: Choices.movie_genre = Option.movie_genre,
        nsfw: Choices.boolean = Option.nsfw,
        year: int = Option.year,
        min_year: int = Option.min_year,
        max_year: int = Option.max_year,
        min_votes: int = Option.min_votes,
        max_votes: int = Option.max_votes,
        min_rating: float = Option.min_rating,
        max_rating: float = Option.max_rating,
        min_runtime: int = Option.min_runtime,
        max_runtime: int = Option.max_runtime,
        page: int = Option.page,
    ) -> None:
        """Subcommand to discover movies by different types of data."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        discover = TMDB.discover(language=language, region=region)
        results = await discover.movies(
            page=page,
            include_adult=nsfw,
            sort_by=sort_by,
            with_watch_providers=service,
            with_genres=genre,
            year=year if year != -1 else None,
            primary_release_date__gte=f"{min_year}-01-01" if min_year != -1 else None,
            primary_release_date__lte=f"{max_year}-12-31" if max_year != -1 else None,
            vote_count__gte=min_votes if min_votes != -1 else None,
            vote_count__lte=max_votes if max_votes != -1 else None,
            vote_average__gte=min_rating if min_rating != -1 else None,
            vote_average__lte=max_rating if max_rating != -1 else None,
            with_runtime__gte=min_runtime if min_runtime != -1 else None,
            with_runtime__lte=max_runtime if max_runtime != -1 else None,
        )
        await self._reply(
            inter,
            results=results,
            page=discover.page,
            total_pages=discover.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["popular_movie"]["description"])
    async def popular(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand to get the current popular movies."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        movie = TMDB.movie(language=language, region=region)
        results = await movie.popular(page=page)
        await self._reply(
            inter,
            results=results,
            page=movie.page,
            total_pages=movie.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["search_movie"]["description"])
    async def search(
        self,
        inter: ApplicationCommandInteraction,
        query: str = Option.query,
        year: int = Option.year,
        nsfw: Choices.boolean = Option.nsfw,
        page: int = Option.page,
    ) -> None:
        """Subcommand to search for a movie."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        search = TMDB.search(language=language, region=region)
        results = await search.movies(query, page=page, include_adult=nsfw, year=year)
        await self._reply(
            inter,
            results=results,
            page=search.page,
            total_pages=search.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["top_movie"]["description"])
    async def top(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand get the top rated movies."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        movie = TMDB.movie(language=language, region=region)
        results = await movie.top_rated(page=page)
        await self._reply(
            inter,
            results=results,
            page=movie.page,
            total_pages=movie.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["trending_movie"]["description"])
    async def trending(
        self, inter: ApplicationCommandInteraction, interval: Choices.interval = Option.interval
    ) -> None:
        """Subcommand get the trending movies."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        trending = TMDB.trending(language=language, region=region)
        if interval == "day":
            results = await trending.movies_day()
        else:
            results = await trending.movies_week()
        await self._reply(
            inter,
            results=results,
            page=trending.page,
            total_pages=trending.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["upcoming_movie"]["description"])
    async def upcoming(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand get the upcoming movies in theatres."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        movie = TMDB.movie(language=language, region=region)
        results = await movie.upcoming(page=page)
        await self._reply(
            inter,
            results=results.results,
            page=movie.page,
            total_pages=movie.total_pages,
            language=language,
            region=region,
        )


def setup(bot: Bot) -> None:
    """Setup `Movies` cog."""
    bot.add_cog(Movies(bot))
