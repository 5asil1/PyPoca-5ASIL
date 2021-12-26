# -*- coding: utf-8 -*-
from typing import List, Union

from disnake import MessageInteraction
from disnake.ext.commands import Bot
from disnake.ui import Button, View

from pypoca.entities import TV, Movie, Person
from pypoca.languages import Language

__all__ = "Buttons"


class Buttons(View):
    def __init__(
        self,
        bot: Bot,
        entity: Union[Movie, Person, TV] = None,
        *,
        language: str = None,
        region: str = None,
    ) -> None:
        self._bot = bot
        self._entity = entity
        self._language = language
        self._quotes = Language(language)
        self._region = region
        if isinstance(entity, Movie):
            buttons = self.from_movie(entity, self._quotes)
        elif isinstance(entity, Person):
            buttons = self.from_person(entity, self._quotes)
        elif isinstance(entity, TV):
            buttons = self.from_tv(entity, self._quotes)
        else:
            raise Exception()
        super().__init__()
        for data in buttons:
            button = Button(**data)
            button.callback = getattr(self, f"callback_{button.custom_id}", None)
            self.add_item(button)

    @staticmethod
    def from_movie(movie: Movie, quotes: Language) -> List[dict]:
        """Convert a `entities.Movie` to a list of `disnake.Button` dict data."""
        return [
            {
                "style": 5,
                "label": quotes.commands["movie"]["reply"]["buttons"]["trailer"],
                "url": movie.trailer,
                "disabled": not movie.youtube_id,
            },
            {
                "style": 5,
                "label": "IMDb",
                "url": movie.imdb,
                "disabled": not movie.imdb_id,
            },
            {
                "style": 2,
                "label": quotes.commands["movie"]["reply"]["buttons"]["cast"],
                "custom_id": "cast",
                "disabled": not movie.cast,
            },
            {
                "style": 2,
                "label": quotes.commands["movie"]["reply"]["buttons"]["crew"],
                "custom_id": "crew",
                "disabled": not movie.crew,
            },
            {
                "style": 2,
                "label": quotes.commands["movie"]["reply"]["buttons"]["similar"],
                "custom_id": "similar_movie",
                "disabled": not movie.recommendations,
            },
        ]

    @staticmethod
    def from_tv(tv: TV, quotes: Language) -> List[dict]:
        """Convert a `entities.TV` to a list of `disnake.Button` dict data."""
        return [
            {
                "style": 5,
                "label": quotes.commands["tv"]["reply"]["buttons"]["trailer"],
                "url": tv.trailer,
                "disabled": not tv.youtube_id,
            },
            {
                "style": 5,
                "label": "IMDb",
                "url": tv.imdb,
                "disabled": not tv.imdb_id,
            },
            {
                "style": 2,
                "label": quotes.commands["tv"]["reply"]["buttons"]["cast"],
                "custom_id": "cast",
                "disabled": not tv.cast,
            },
            {
                "style": 2,
                "label": quotes.commands["tv"]["reply"]["buttons"]["crew"],
                "custom_id": "crew",
                "disabled": not tv.crew,
            },
            {
                "style": 2,
                "label": quotes.commands["tv"]["reply"]["buttons"]["similar"],
                "custom_id": "similar_tv",
                "disabled": not tv.recommendations,
            },
        ]

    @staticmethod
    def from_person(person: Person, quotes: Language) -> List[dict]:
        """Convert a `entities.Person` to a list of `disnake.Button` dict data."""
        return [
            {
                "style": 5,
                "label": "IMDb",
                "url": person.imdb,
                "disabled": person.imdb_id is None,
            },
            {
                "style": 5,
                "label": "Instagram",
                "url": person.instagram,
                "disabled": person.instagram_id is None,
            },
            {
                "style": 5,
                "label": "Twitter",
                "url": person.twitter,
                "disabled": person.twitter_id is None,
            },
            {
                "style": 2,
                "label": quotes.commands["person"]["reply"]["buttons"]["acting"],
                "custom_id": "acting",
                "disabled": not person.cast,
            },
            {
                "style": 2,
                "label": quotes.commands["person"]["reply"]["buttons"]["jobs"],
                "custom_id": "jobs",
                "disabled": not person.crew,
            },
        ]

    async def callback_cast(self, inter: MessageInteraction) -> None:
        """Called in case the cast button was clicked."""
        inter.bot = self._bot
        await self._bot.get_cog("People")._reply(
            inter,
            results=self._entity.cast[:20],
            page=1,
            total_pages=len(self._entity.cast) // 20,
            language=self._language,
            region=self._region,
        )

    async def callback_crew(self, inter: MessageInteraction) -> None:
        """Called in case the crew button was clicked."""
        inter.bot = self._bot
        await self._bot.get_cog("People")._reply(
            inter,
            results=self._entity.crew[:20],
            page=1,
            total_pages=len(self._entity.crew) // 20,
            language=self._language,
            region=self._region,
        )

    async def callback_similar_movie(self, inter: MessageInteraction) -> None:
        """Called in case the similar button was clicked."""
        inter.bot = self._bot
        await self._bot.get_cog("Movies")._reply(
            inter,
            results=self._entity.recommendations[:20],
            page=1,
            total_pages=len(self._entity.recommendations) // 20,
            language=self._language,
            region=self._region,
        )

    async def callback_similar_tv(self, inter: MessageInteraction) -> None:
        """Called in case the similar button was clicked."""
        inter.bot = self._bot
        await self._bot.get_cog("TVs")._reply(
            inter,
            results=self._entity.recommendations[:20],
            page=1,
            total_pages=len(self._entity.recommendations) // 20,
            language=self._language,
            region=self._region,
        )

    async def callback_acting(self, inter: MessageInteraction) -> None:
        """Called in case the acting button was clicked."""
        if len(self._entity.cast_movie) >= len(self._entity.cast_tv):
            cog = self._bot.get_cog("Movies")
            results = self._entity.cast_movie
        else:
            cog = self._bot.get_cog("TVs")
            results = self._entity.cast_tv
        inter.bot = self._bot
        await cog._reply(
            inter,
            results=results[:20],
            page=1,
            total_pages=len(results) // 20,
            language=self._language,
            region=self._region,
        )

    async def callback_jobs(self, inter: MessageInteraction) -> None:
        """Called in case the jobs button was clicked."""
        if len(self._entity.crew_movie) >= len(self._entity.crew_tv):
            cog = self._bot.get_cog("Movies")
            results = self._entity.crew_movie
        else:
            cog = self._bot.get_cog("TVs")
            results = self._entity.crew_tv
        inter.bot = self._bot
        await cog._reply(
            inter,
            results=results[:20],
            page=1,
            total_pages=len(results) // 20,
            language=self._language,
            region=self._region,
        )
