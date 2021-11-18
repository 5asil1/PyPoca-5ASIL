# -*- coding: utf-8 -*-
from aiotmdb import TMDB
from discord.ext.commands import Bot, Cog
from dislash import ResponseType, SlashInteraction, slash_command

from pypoca.adapters import Adapter
from pypoca.config import TMDBConfig
from pypoca.embeds import Option, Buttons, Poster, Menu
from pypoca.exceptions import NotFound
from pypoca.languages import CommandDescription


class Person(Cog):
    """`Person` cog has all person related commands."""

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
        adapter = Adapter("person")
        if len(results) > 1:
            embed = Poster(title="People results")
            select_menu = Menu(options=[adapter.option(result) for result in results])
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
        person_id = results[index].id
        result = await TMDB.person(language=language, region=region).details(
            person_id,
            append_to_response="combined_credits,external_ids",
        )
        embed = Poster(**adapter.embed(result, region=region))
        buttons = Buttons(buttons=adapter.buttons(result))
        if len(results) > 1:
            await ctx.reply(embed=embed, components=[buttons], type=ResponseType.UpdateMessage)
        else:
            await inter.reply(embed=embed, components=[buttons])

    @slash_command(name="people", description=CommandDescription.person)
    async def person(self, inter: SlashInteraction):
        """Command that groups person-related subcommands."""

    @person.sub_command(
        name="popular",
        description=CommandDescription.popular_person,
        options=[Option.page, Option.language, Option.region],
        connectors={Option.page.name: "page", Option.language.name: "language", Option.region.name: "region"},
    )
    async def popular_person(
        self,
        inter: SlashInteraction,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to get the current popular person."""
        person = TMDB.person(language=language, region=region)
        results = await person.popular(page=page)
        await self._reply(
            inter,
            results=results,
            page=person.page,
            total_pages=person.total_pages,
            language=language,
            region=region,
        )

    @person.sub_command(
        name="search",
        description=CommandDescription.search_person,
        options=[
            Option.query,
            Option.nsfw,
            Option.page,
            Option.language,
            Option.region,
        ],
        connectors={
            Option.query.name: "query",
            Option.nsfw.name: "nsfw",
            Option.page.name: "page",
            Option.language.name: "language",
            Option.region.name: "region",
        },
    )
    async def search_person(
        self,
        inter: SlashInteraction,
        query: str,
        nsfw: bool = False,
        page: int = 1,
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand to search for a person."""
        search = TMDB.search(language=language, region=region)
        results = await search.person(query, page=page, include_adult=nsfw)
        await self._reply(
            inter,
            results=results,
            page=search.page,
            total_pages=search.total_pages,
            language=language,
            region=region,
        )

    @person.sub_command(
        name="trending",
        description=CommandDescription.trending_person,
        options=[Option.interval, Option.language, Option.region],
        connectors={Option.interval.name: "interval", Option.language.name: "language", Option.region.name: "region"},
    )
    async def trending_person(
        self,
        inter: SlashInteraction,
        interval: str = "day",
        language: str = TMDBConfig.language,
        region: str = TMDBConfig.region,
    ) -> None:
        """Subcommand get the trending persons."""
        trending = TMDB.trending(language=language, region=region)
        if interval == "day":
            results = await trending.person_day()
        else:
            results = await trending.person_week()
        await self._reply(
            inter,
            results=results,
            page=trending.page,
            total_pages=trending.total_pages,
            language=language,
            region=region,
        )


def setup(bot: Bot) -> None:
    """Setup `Person` cog."""
    bot.add_cog(Person(bot))