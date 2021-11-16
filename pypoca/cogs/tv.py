# -*- coding: utf-8 -*-
from typing import List

from aiotmdb import TMDB, AsObj
from discord.ext.commands import Bot, Cog
from dislash import ResponseType, SlashInteraction, slash_command

from pypoca import utils
from pypoca.config import TMDBConfig
from pypoca.embeds import Option, ReplyButtons, ReplyEmbed, ReplyMenu
from pypoca.exceptions import NotFound
from pypoca.languages import CommandDescription


class TV(Cog):
    """`TV` cog has all TV show related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def _tv(result: AsObj, region: str) -> dict:
        vote_average = result.get("vote_average")
        vote_count = result.get("vote_count")
        genres = [genre["name"] for genre in result.get("genres", [])]
        networks = [network["name"] for network in result.get("networks", [])]
        rating = f"{vote_average} ({vote_count} votes)" if vote_average else None
        status = result.get("status")
        first_air_date = utils.format_datetime(result.first_air_date)
        last_air_date = utils.format_datetime(result.last_air_date)
        number_of_episodes = result.get("number_of_episodes", 0)
        number_of_seasons = result.get("number_of_seasons", 0)
        episode_run_time = (
            sum(result.episode_run_time) / len(result.episode_run_time) if result.get("episode_run_time") else 0
        )
        total_duration = utils.format_duration(episode_run_time * number_of_episodes)
        duration = utils.format_duration(episode_run_time)
        try:
            watch_providers = [
                watch_provider["provider_name"]
                for watch_provider in result["watch/providers"]["results"][region]["flatrate"]
            ]
        except Exception:
            watch_providers = []

        tv = {
            "title": result.get("name", result.original_name),
            "description": result.get("overview"),
            "fields": [
                {"name": "Rating", "value": rating or "-"},
                {"name": "Premiered", "value": first_air_date or "-"},
                {
                    "name": "Status",
                    "value": f"{status} ({last_air_date})" if status == "Ended" else status if status else "-",
                },
                {"name": "Episodes", "value": number_of_episodes or "-"},
                {"name": "Seasons", "value": number_of_seasons or "-"},
                {"name": "Runtime", "value": f"{duration} ({total_duration} total)"},
                {"name": "Genre", "value": ", ".join(genres) if genres else "-"},
                {"name": "Network", "value": networks[0] if networks else "-"},
                {"name": "Watch on", "value": ", ".join(watch_providers) if watch_providers else "-"},
            ],
        }
        if result.get("homepage"):
            tv["url"] = result.homepage
        if result.get("backdrop_path"):
            tv["image"] = {"url": f"https://image.tmdb.org/t/p/w1280/{result.backdrop_path}"}
        if result.get("created_by"):
            director = result.created_by[0]
            tv["author"] = {"name": director.name}
            if director.get("profile_path"):
                tv["author"]["icon_url"] = f"https://image.tmdb.org/t/p/w185/{director.profile_path}"
        return tv

    @staticmethod
    def _option(result: AsObj) -> dict:
        title = result.get("name", result.original_name)
        release_date = utils.format_datetime(result.get("first_air_date"))
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
            {"label": "Watch", "url": f"https://embed.warezcdn.net/serie/{imdb_id}"},
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
            embed = ReplyEmbed(title="TV show results")
            select_menu = ReplyMenu(options=[self._option(result) for result in results])
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
        tv_id = results[index].id
        result = await TMDB.tv(language=language, region=region).details(
            tv_id,
            append_to_response="credits,external_ids,recommendations,videos,watch/providers",
        )
        embed = ReplyEmbed(**self._tv(result, region=region))
        buttons = ReplyButtons(buttons=self._buttons(result))
        if len(results) > 1:
            await ctx.reply(embed=embed, components=[buttons], type=ResponseType.UpdateMessage)
        else:
            await inter.reply(embed=embed, components=[buttons])

    @slash_command(name="tv", description=CommandDescription.tv)
    async def tv(self, inter: SlashInteraction):
        """Command that groups tv-related subcommands."""

    @tv.sub_command(
        name="discover",
        description=CommandDescription.discover_tv,
        options=[
            Option.tv_sort_by,
            Option.tv_service,
            Option.tv_genre,
            Option.year,
            Option.min_year,
            Option.max_year,
            Option.min_votes,
            Option.min_rating,
            Option.min_runtime,
            Option.max_runtime,
            Option.page,
            Option.language,
            Option.region,
        ],
    )
    async def discover_tv(
        self,
        inter: SlashInteraction,
        sort_by: str = "popularity.desc",
        service: str = None,
        genre: str = None,
        year: int = None,
        min_year: int = None,
        max_year: int = None,
        min_votes: int = None,
        min_rating: float = None,
        min_runtime: int = None,
        max_runtime: int = None,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to discover TV shows by different types of data."""
        discover = TMDB.discover(language=language, region=region)
        results = await discover.tv_shows(
            page=page,
            sort_by=sort_by,
            with_watch_providers=service,
            with_genres=genre,
            first_air_date_year=year,
            first_air_date__gte=f"{min_year}-01-01" if min_year else None,
            first_air_date__lte=f"{max_year}-12-31" if max_year else None,
            vote_count__gte=min_votes,
            vote_average__gte=min_rating,
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

    @tv.sub_command(
        name="popular",
        description=CommandDescription.popular_tv,
        options=[Option.page, Option.language, Option.region],
    )
    async def popular_tv(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to get the current popular TV shows."""
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

    @tv.sub_command(
        name="search",
        description=CommandDescription.search_tv,
        options=[
            Option.query,
            Option.year,
            Option.nsfw,
            Option.page,
            Option.language,
            Option.region,
        ],
    )
    async def search_tv(
        self,
        inter: SlashInteraction,
        query: str,
        year: int = None,
        nsfw: bool = False,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to search for a TV show."""
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

    @tv.sub_command(
        name="top",
        description=CommandDescription.top_tv,
        options=[Option.page, Option.language, Option.region],
    )
    async def top_tv(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the top rated TV shows."""
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

    @tv.sub_command(
        name="trending",
        description=CommandDescription.trending_tv,
        options=[Option.interval, Option.language, Option.region],
    )
    async def trending_tv(
        self,
        inter: SlashInteraction,
        interval: str = "day",
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the trending TV shows."""
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

    @tv.sub_command(
        name="upcoming",
        description=CommandDescription.upcoming_tv,
        options=[Option.page, Option.language, Option.region],
    )
    async def upcoming_tv(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the upcoming TV shows in theatres."""
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
    """Setup `TV` cog."""
    bot.add_cog(TV(bot))
