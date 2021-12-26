# -*- coding: utf-8 -*-
from typing import List

from aiotmdb import TMDB
from disnake import ApplicationCommandInteraction, Embed
from disnake.ext.commands import Bot, Cog, slash_command

from pypoca import utils
from pypoca.embeds import Choices, Menu, Option
from pypoca.entities import TV, Color
from pypoca.exceptions import NotFound
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("TVs", "setup")


class TVs(Cog):
    """`TVs` cog has all TV show related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def get_tv_by_id(tv_id: int, language: str, region: str) -> TV:
        result = await TMDB.tv(language=language, region=region).details(
            tv_id,
            append_to_response="credits,external_ids,recommendations,videos,watch/providers",
        )
        try:
            result["external_ids"]["trakt_id"] = await utils.get_trakt_id(tv_id, type="show")
        except Exception:
            result["external_ids"]["trakt_id"] = None
        result["id"] = tv_id
        return TV.from_tmdb(result)

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
        tv_shows = [TV.from_tmdb(result) for result in results]
        embed = Embed(title=quotes.commands["tv"]["reply"]["title"], color=Color.bot)
        menu = Menu(inter.bot, tv_shows, callback=TVs.get_tv_by_id, language=language, region=region)
        await inter.send(embed=embed, view=menu)

    @slash_command(name="tv", description=DEFAULT_LANGUAGE.commands["tv"]["description"])
    async def tv(self, inter: ApplicationCommandInteraction):
        """Command that groups tv-related subcommands."""

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["discover_tv"]["description"])
    async def discover(
        self,
        inter: ApplicationCommandInteraction,
        sort_by: Choices.tv_sort_by = Option.tv_sort_by,
        service: Choices.tv_service = Option.tv_service,
        genre: Choices.tv_genre = Option.tv_genre,
        year: int = Option.year,
        min_year: int = Option.min_year,
        max_year: int = Option.max_year,
        min_votes: int = Option.min_votes,
        min_rating: float = Option.min_rating,
        min_runtime: int = Option.min_runtime,
        max_runtime: int = Option.max_runtime,
        page: int = Option.page,
    ) -> None:
        """Subcommand to discover TV shows by different types of data."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        discover = TMDB.discover(language=language, region=region)
        results = await discover.tv_shows(
            page=page,
            sort_by=sort_by,
            with_watch_providers=service,
            with_genres=genre,
            first_air_date_year=year if year != -1 else None,
            first_air_date__gte=f"{min_year}-01-01" if min_year != -1 else None,
            first_air_date__lte=f"{max_year}-12-31" if max_year != -1 else None,
            vote_count__gte=min_votes if min_votes != -1 else None,
            vote_average__gte=min_rating if min_rating != -1 else None,
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

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["popular_tv"]["description"])
    async def popular(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand to get the current popular TV shows."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        tv = TMDB.tv(language=language, region=region)
        results = await tv.popular(page=page)
        await self._reply(
            inter,
            results=results,
            page=tv.page,
            total_pages=tv.total_pages,
            language=language,
            region=region,
        )

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["search_tv"]["description"])
    async def search(
        self,
        inter: ApplicationCommandInteraction,
        query: str = Option.query,
        year: int = Option.year,
        nsfw: Choices.boolean = Option.nsfw,
        page: int = Option.page,
    ) -> None:
        """Subcommand to search for a TV show."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        search = TMDB.search(language=language, region=region)
        results = await search.tv_shows(query, page=page, include_adult=nsfw, first_air_date_year=year)
        await self._reply(
            inter,
            results=results,
            page=search.page,
            total_pages=search.total_pages,
            language=language,
            region=region,
        )

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["top_tv"]["description"])
    async def top(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand get the top rated TV shows."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        tv = TMDB.tv(language=language, region=region)
        results = await tv.top_rated(page=page)
        await self._reply(
            inter,
            results=results,
            page=tv.page,
            total_pages=tv.total_pages,
            language=language,
            region=region,
        )

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["trending_tv"]["description"])
    async def trending(
        self, inter: ApplicationCommandInteraction, interval: Choices.interval = Option.interval
    ) -> None:
        """Subcommand get the trending TV shows."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        trending = TMDB.trending(language=language, region=region)
        if interval == "day":
            results = await trending.tv_shows_day()
        else:
            results = await trending.tv_shows_week()
        await self._reply(
            inter,
            results=results,
            page=trending.page,
            total_pages=trending.total_pages,
            language=language,
            region=region,
        )

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["upcoming_tv"]["description"])
    async def upcoming(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand get the upcoming TV shows in theatres."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
        tv = TMDB.tv(language=language, region=region)
        results = await tv.on_the_air(page=page)
        await self._reply(
            inter,
            results=results,
            page=tv.page,
            total_pages=tv.total_pages,
            language=language,
            region=region,
        )


def setup(bot: Bot) -> None:
    """Setup `TVs` cog."""
    bot.add_cog(TVs(bot))
