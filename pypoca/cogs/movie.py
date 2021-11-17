# -*- coding: utf-8 -*-
from typing import List

from aiotmdb import TMDB, AsObj
from discord.ext.commands import Bot, Cog
from dislash import ResponseType, SlashInteraction, slash_command

from pypoca import utils
from pypoca.config import TMDBConfig
from pypoca.embeds import Option, Buttons, Poster, Menu
from pypoca.exceptions import NotFound
from pypoca.languages import CommandDescription


class Movie(Cog):
    """`Movie` cog has all movie related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _movie(result: AsObj, region: str) -> dict:
        vote_average = result.get("vote_average")
        vote_count = result.get("vote_count")
        genres = [genre["name"] for genre in result.get("genres", [])]
        production_companies = [company["name"] for company in result.get("production_companies", [])]
        rating = f"{vote_average} ({vote_count} votes)" if vote_average else None
        release_date = utils.format_datetime(result.release_date) or result.get("status")
        duration = utils.format_duration(result.get("runtime"))
        try:
            watch_providers = [
                watch_provider["provider_name"]
                for watch_provider in result["watch/providers"]["results"][region]["flatrate"]
            ]
        except Exception:
            watch_providers = []

        movie = {
            "title": result.get("title", result.original_title),
            "description": result.get("overview"),
            "fields": [
                {"name": "Rating", "value": rating or "-"},
                {"name": "Released", "value": release_date or "-"},
                {"name": "Watch on", "value": ", ".join(watch_providers) if watch_providers else "-"},
                {"name": "Runtime", "value": duration or "-"},
                {"name": "Genre", "value": ", ".join(genres) if genres else "-"},
                {"name": "Studios", "value": production_companies[0] if production_companies else "-"},
            ],
        }
        if result.get("homepage"):
            movie["url"] = result.homepage
        if result.get("backdrop_path"):
            movie["image"] = {"url": f"https://image.tmdb.org/t/p/w1280/{result.backdrop_path}"}
        for person in result.credits.get("crew", []):
            if person["job"] == "Director":
                movie["author"] = {"name": person.name}
                if person.get("profile_path"):
                    movie["author"]["icon_url"] = f"https://image.tmdb.org/t/p/w185/{person.profile_path}"
                break
        return movie

    @staticmethod
    def _option(result: AsObj) -> dict:
        title = result.get("title", result.original_title)
        release_date = utils.format_datetime(result.get("release_date"))
        vote_average = result.get("vote_average")
        vote_count = result.get("vote_count")
        label = f"{title} ({release_date})" if release_date else title
        description = f"{vote_average} ({vote_count} votes)" if vote_average else ""
        return {"label": label[:100], "description": description[:100]}

    @staticmethod
    def _buttons(result: AsObj) -> List[dict]:
        imdb_id = result.external_ids.get("imdb_id")
        try:
            video_key = result.videos["results"][0]["key"]
        except Exception:
            video_key = None
        buttons = [
            {"label": "Trailer", "url": f"https://www.youtube.com/watch?v={video_key}"},
            {"label": "Watch", "url": f"https://embed.warezcdn.net/filme/{imdb_id}"},
            {"label": "IMDb", "url": f"https://www.imdb.com/title/{imdb_id}"},
        ]
        return buttons

    async def _reply(
        self,
        inter: SlashInteraction,
        *,
        results: List[AsObj],
        page: int,
        total_pages: int,
        language: str,
        region: str,
    ) -> None:
        if len(results) > 1:
            embed = Poster(title="Movie results")
            select_menu = Menu(options=[self._option(result) for result in results])
            msg = await inter.reply(
                embed=embed,
                components=[select_menu],
                type=ResponseType.ChannelMessageWithSource,
            )

            def check(ctx: SlashInteraction):
                return ctx.author == inter.author

            ctx = await msg.wait_for_dropdown(check)
            index = int(ctx.select_menu.selected_options[0].value)
        elif len(results) == 1:
            index = 0
        else:
            raise NotFound()
        movie_id = results[index].id
        result = await TMDB.movie(language=language, region=region).details(
            movie_id,
            append_to_response="credits,external_ids,recommendations,videos,watch/providers",
        )
        embed = Poster(**self._movie(result, region=region))
        buttons = Buttons(buttons=self._buttons(result))
        if len(results) > 1:
            await ctx.reply(embed=embed, components=[buttons], type=ResponseType.UpdateMessage)
        else:
            await inter.reply(embed=embed, components=[buttons])

    @slash_command(name="movie", description=CommandDescription.movie)
    async def movie(self, inter: SlashInteraction):
        """Command that groups movie-related subcommands."""

    @movie.sub_command(
        name="discover",
        description=CommandDescription.discover_movie,
        options=[
            Option.movie_sort_by,
            Option.movie_service,
            Option.movie_genre,
            Option.nsfw,
            Option.year,
            Option.min_year,
            Option.max_year,
            Option.min_votes,
            Option.max_votes,
            Option.min_rating,
            Option.max_rating,
            Option.min_runtime,
            Option.max_runtime,
            Option.page,
            Option.language,
            Option.region,
        ],
    )
    async def discover_movie(
        self,
        inter: SlashInteraction,
        sort_by: str = "popularity.desc",
        service: str = None,
        genre: str = None,
        nsfw: bool = False,
        year: int = None,
        min_year: int = None,
        max_year: int = None,
        min_votes: int = None,
        max_votes: int = None,
        min_rating: float = None,
        max_rating: float = None,
        min_runtime: int = None,
        max_runtime: int = None,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to discover movies by different types of data."""
        discover = TMDB.discover(language=language, region=region)
        results = await discover.movies(
            page=page,
            include_adult=nsfw,
            sort_by=sort_by,
            with_watch_providers=service,
            with_genres=genre,
            year=year,
            primary_release_date__gte=f"{min_year}-01-01" if min_year else None,
            primary_release_date__lte=f"{max_year}-12-31" if max_year else None,
            vote_count__gte=min_votes,
            vote_count__lte=max_votes,
            vote_average__gte=min_rating,
            vote_average__lte=max_rating,
            with_runtime__gte=min_runtime,
            with_runtime__lte=max_runtime,
        )
        await self._reply(
            inter,
            results=results,
            page=discover.page,
            total_pages=discover.total_pages,
            language=language,
            region=region,
        )

    @movie.sub_command(
        name="popular",
        description=CommandDescription.popular_movie,
        options=[Option.page, Option.language, Option.region],
    )
    async def popular_movie(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to get the current popular movies."""
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

    @movie.sub_command(
        name="search",
        description=CommandDescription.search_movie,
        options=[
            Option.query,
            Option.year,
            Option.nsfw,
            Option.page,
            Option.language,
            Option.region,
        ],
    )
    async def search_movie(
        self,
        inter: SlashInteraction,
        query: str,
        year: int = None,
        nsfw: bool = False,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to search for a movie."""
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

    @movie.sub_command(
        name="top",
        description=CommandDescription.top_movie,
        options=[Option.page, Option.language, Option.region],
    )
    async def top_movie(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the top rated movies."""
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

    @movie.sub_command(
        name="trending",
        description=CommandDescription.trending_movie,
        options=[Option.interval, Option.language, Option.region],
    )
    async def trending_movie(
        self,
        inter: SlashInteraction,
        interval: str = "day",
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the trending movies."""
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

    @movie.sub_command(
        name="upcoming",
        description=CommandDescription.upcoming_movie,
        options=[Option.page, Option.language, Option.region],
    )
    async def upcoming_movie(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the upcoming movies in theatres."""
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
    """Setup `Movie` cog."""
    bot.add_cog(Movie(bot))
