# -*- coding: utf-8 -*-
from typing import Coroutine, List, Union

from disnake import MessageInteraction, SelectOption
from disnake.ext.commands import Bot
from disnake.ui import Select, View

from pypoca.embeds import Buttons, Content
from pypoca.entities import TV, Movie, Person
from pypoca.languages import Language

__all__ = "Menu"


class Dropdown(Select):
    def __init__(
        self,
        bot: Bot,
        entities: List[Union[Movie, Person, TV]],
        *,
        callback: Coroutine,
        language: str,
        region: str,
    ) -> None:
        self._bot = bot
        self._entities = entities
        self._callback = callback
        self._language = language
        self._quotes = Language(language)
        self._region = region
        if isinstance(entities, list) and isinstance(entities[0], Movie):
            data = self.from_movie(entities)
        elif isinstance(entities, list) and isinstance(entities[0], Person):
            data = self.from_person(entities)
        elif isinstance(entities, list) and isinstance(entities[0], TV):
            data = self.from_tv(entities)
        else:
            raise Exception()
        options = [SelectOption(**option) for option in data]
        super().__init__(placeholder=self._quotes.placeholder, options=options)

    @staticmethod
    def from_movie(movies: List[Movie]) -> List[dict]:
        """Convert a list of `entities.Movie` to a list of `disnake.SelectOption` dict data."""
        return [
            {
                "label": movie.name_and_year,
                "description": movie.rating_and_votes or "",
                "value": i,
            }
            for i, movie in enumerate(movies)
        ]

    @staticmethod
    def from_tv(tvs: List[TV]) -> List[dict]:
        """Convert a list of `entities.TV` to a list of `disnake.SelectOption` dict data."""
        return [
            {
                "label": tv.name_and_year,
                "description": tv.rating_and_votes or "",
                "value": i,
            }
            for i, tv in enumerate(tvs)
        ]

    @staticmethod
    def from_person(people: List[Person]) -> List[dict]:
        """Convert a list of `entities.Person` to a list of `disnake.SelectOption` dict data."""
        return [
            {
                "label": person.name,
                "description": (
                    person.character if person.character else person.job if person.job else person.jobs[:100] or ""
                ),
                "value": i,
            }
            for i, person in enumerate(people)
        ]

    async def callback(self, inter: MessageInteraction) -> None:
        entity_selected = int(self.values[0])
        entity_id = self._entities[entity_selected].id
        entity = await self._callback(entity_id, language=self._language, region=self._region)
        embed = Content(entity, language=self._language, region=self._region)
        view = Buttons(self._bot, entity, language=self._language, region=self._region)
        await inter.send(embed=embed, view=view)


class Menu(View):
    def __init__(
        self,
        bot: Bot,
        entities: List[Union[Movie, Person, TV]],
        *,
        callback: Coroutine,
        language: str,
        region: str,
    ) -> None:
        super().__init__()
        dropdown = Dropdown(bot, entities, callback=callback, language=language, region=region)
        self.add_item(dropdown)
