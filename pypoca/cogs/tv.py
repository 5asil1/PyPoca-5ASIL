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

__all__ = ("TV", "setup")


class TV(Cog):
    """`TV` cog has all TV show related commands."""

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
        adapter = Adapter("tv")
        if len(results) > 1:
            title = quotes.commands["tv"]["reply"]["title"]
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

            ctx = await msg.wait_for_dropdown(check, timeout=120)
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
        try:
            result["external_ids"]["trakt"] = await utils.get_trakt_id(tv_id, type="show")
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
            await TV._reply(
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

    @slash_command(name="tv", description=DEFAULT_LANGUAGE.commands["tv"]["description"])
    async def tv(self, inter: SlashInteraction):
        """Command that groups tv-related subcommands."""

    @tv.sub_command(description=DEFAULT_LANGUAGE.commands["discover_tv"]["description"])
    async def discover(
        self,
        inter: SlashInteraction,
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
    async def popular(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
        inter: SlashInteraction,
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
    async def top(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
    async def trending(self, inter: SlashInteraction, interval: Choices.interval = Option.interval) -> None:
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
    async def upcoming(self, inter: SlashInteraction, page: int = Option.page) -> None:
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
    """Setup `TV` cog."""
    bot.add_cog(TV(bot))
