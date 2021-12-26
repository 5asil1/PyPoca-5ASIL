# -*- coding: utf-8 -*-
from typing import List

from aiotmdb import TMDB
from disnake import ApplicationCommandInteraction, Embed
from disnake.ext.commands import Bot, Cog, slash_command

from pypoca.embeds import Choices, Menu, Option
from pypoca.entities import Color, Person
from pypoca.exceptions import NotFound
from pypoca.languages import DEFAULT_LANGUAGE, Language

__all__ = ("People", "setup")


class People(Cog):
    """`People` cog has all person related commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def get_person_by_id(person_id: int, language: str, region: str) -> Person:
        result = await TMDB.person(language=language, region=region).details(
            person_id,
            append_to_response="combined_credits,movie_credits,tv_credits,external_ids",
        )
        result["id"] = person_id
        return Person.from_tmdb(result)

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
        people = [Person.from_tmdb(result) for result in results]
        embed = Embed(title=quotes.commands["person"]["reply"]["title"], color=Color.bot)
        menu = Menu(inter.bot, people, callback=People.get_person_by_id, language=language, region=region)
        await inter.send(embed=embed, view=menu)

    @slash_command(name="people", description=DEFAULT_LANGUAGE.commands["person"]["description"])
    async def person(self, inter: ApplicationCommandInteraction):
        """Command that groups person-related subcommands."""

    @person.sub_command(description=DEFAULT_LANGUAGE.commands["popular_person"]["description"])
    async def popular(self, inter: ApplicationCommandInteraction, page: int = Option.page) -> None:
        """Subcommand to get the current popular person."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
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

    @person.sub_command(description=DEFAULT_LANGUAGE.commands["search_person"]["description"])
    async def search(
        self,
        inter: ApplicationCommandInteraction,
        query: str = Option.query,
        nsfw: Choices.boolean = Option.nsfw,
        page: int = Option.page,
    ) -> None:
        """Subcommand to search for a person."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
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

    @person.sub_command(description=DEFAULT_LANGUAGE.commands["trending_person"]["description"])
    async def trending(
        self,
        inter: ApplicationCommandInteraction,
        interval: Choices.interval = Option.interval,
    ) -> None:
        """Subcommand get the trending persons."""
        language = self.bot.servers[inter.guild_id]["language"]
        region = self.bot.servers[inter.guild_id]["region"]
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
    """Setup `People` cog."""
    bot.add_cog(People(bot))
