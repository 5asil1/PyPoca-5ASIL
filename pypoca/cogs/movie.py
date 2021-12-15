# -*- coding: utf-8 -*-
from aiotmdb import TMDB
from discord import Embed
from discord.ext.commands import Bot, Cog
from dislash import ActionRow, Button, ResponseType, SelectMenu, SlashInteraction, slash_command

from pypoca import utils
from pypoca.adapters import Adapter
from pypoca.embeds import Choices, Color, Option
from pypoca.exceptions import NotFound
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("Movie", "setup")


class Movie(Cog):
    """`Movie` cog has all movie related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def _reply(
        inter: SlashInteraction,
        *,
        results: list,
        page: int,
        total_pages: int,
        language: str,
        region: str,
    ) -> None:
        quotes = Language(language)
        adapter = Adapter("movie")
        if len(results) > 1:
            title = quotes.commands["movie"]["reply"]["title"]
            embed = Embed(title=title, color=Color.bot)
            options = [{"value": i, **adapter.option(result, language)} for i, result in enumerate(results)]
            select_menu = SelectMenu.from_dict({"placeholder": quotes.placeholder, "options": options})
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
        try:
            result["external_ids"]["trakt"] = await utils.get_trakt_id(movie_id, type="movie")
        except Exception:
            result["external_ids"]["trakt"] = None
        embed = Embed.from_dict(adapter.embed(result, language, region))
        buttons = adapter.buttons(result, language)
        action_row = ActionRow(*[Button.from_dict(button) for button in buttons])
        if len(results) > 1:
            msg = await ctx.reply(embed=embed, components=[action_row], type=ResponseType.UpdateMessage)
        else:
            msg = await inter.reply(embed=embed, components=[action_row])
        on_click = msg.create_click_listener(timeout=120)

        @on_click.not_from_user(inter.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter: SlashInteraction):
            """Called in case a button was clicked not by the author."""
            pass

        @on_click.matching_id("cast")
        async def on_cast_button(inter: SlashInteraction):
            """Called in case the cast button was clicked."""
            person = inter.bot.get_cog("Person")
            await person._reply(
                inter,
                results=result.credits.cast[:20],
                page=1,
                total_pages=len(result.credits.cast) // 20,
                language=language,
                region=region,
            )

        @on_click.matching_id("crew")
        async def on_crew_button(inter: SlashInteraction):
            """Called in case the crew button was clicked."""
            person = inter.bot.get_cog("Person")
            await person._reply(
                inter,
                results=result.credits.crew[:20],
                page=1,
                total_pages=len(result.credits.crew) // 20,
                language=language,
                region=region,
            )

        @on_click.matching_id("similar")
        async def on_similar_button(inter: SlashInteraction):
            """Called in case the similar button was clicked."""
            await Movie._reply(
                inter,
                results=result.recommendations.results[:20],
                page=1,
                total_pages=len(result.recommendations.results) // 20,
                language=language,
                region=region,
            )

        @on_click.timeout
        async def on_timeout():
            """Waiting for listener timeout."""
            await msg.edit(components=[])

    @slash_command(description=DEFAULT_LANGUAGE.commands["movie"]["description"])
    async def movie(self, inter: SlashInteraction):
        """Command that groups movie-related subcommands."""

    @movie.sub_command(description=DEFAULT_LANGUAGE.commands["discover_movie"]["description"])
    async def discover(
        self,
        inter: SlashInteraction,
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
    async def popular(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
        inter: SlashInteraction,
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
    async def top(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
    async def trending(self, inter: SlashInteraction, interval: Choices.interval = Option.interval) -> None:
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
    async def upcoming(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
    """Setup `Movie` cog."""
    bot.add_cog(Movie(bot))
