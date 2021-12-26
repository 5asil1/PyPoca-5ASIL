# -*- coding: utf-8 -*-
from typing import Union

from disnake import Embed

from pypoca.entities import TV, Color, Movie, Person
from pypoca.languages import Language

__all__ = "Content"


class Content(Embed):
    def __init__(self, entity: Union[Movie, Person, TV], *, language: str, region: str) -> None:
        self._entity = entity
        self._language = language
        self._quotes = Language(language)
        self._region = region
        if isinstance(entity, Movie):
            data = self.from_movie(entity, self._quotes, region)
        elif isinstance(entity, Person):
            data = self.from_person(entity, self._quotes)
        elif isinstance(entity, TV):
            data = self.from_tv(entity, self._quotes, region)
        else:
            raise Exception()
        fields = data.pop("fields", None)
        author = data.pop("author", None)
        image = data.pop("image", None)
        thumbnail = data.pop("thumbnail", None)
        data = {key: value for key, value in data.items() if value is not None}
        super().__init__(**data)
        if fields:
            [self.add_field(**field) for field in fields]
        if author:
            self.set_author(**author)
        if image:
            self.set_image(**image)
        if thumbnail:
            self.set_thumbnail(**thumbnail)

    @staticmethod
    def from_movie(movie: Movie, quotes: Language, region: str) -> dict:
        """Convert a `entities.Movie` to a `discord.Embed` dict data."""
        return {
            "title": movie.title,
            "description": movie.description,
            "color": Color.bot,
            "url": movie.url,
            "image": {"url": movie.image} if movie.image else {},
            "author": {"name": movie.directors} if movie.directors else {},
            "fields": [
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["rating"],
                    "value": movie.rating_and_votes or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["released"],
                    "value": movie.date.strftime(quotes.datetime_format) if movie.date else "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["watch"],
                    "value": movie.watch_on(region) or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["runtime"],
                    "value": movie.duration or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["genre"],
                    "value": movie.genre or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["movie"]["reply"]["fields"]["studios"],
                    "value": movie.studios or "-",
                    "inline": True,
                },
            ],
        }

    @staticmethod
    def from_tv(tv: TV, quotes: Language, region: str) -> dict:
        """Convert a `entities.TV` to a `discord.Embed` dict data."""
        return {
            "title": tv.title,
            "description": tv.description,
            "color": Color.bot,
            "url": tv.url,
            "image": {"url": tv.image} if tv.image else {},
            "author": {"name": tv.directors} if tv.directors else {},
            "fields": [
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["rating"],
                    "value": tv.rating_and_votes or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["premiered"],
                    "value": tv.date.strftime(quotes.datetime_format) if tv.date else "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["status"],
                    "value": (
                        f"{tv.status} ({tv.date_end})" if tv.status == "Ended" else tv.status if tv.status else "-"
                    ),
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["episodes"],
                    "value": str(tv.episodes) or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["seasons"],
                    "value": str(tv.seasons) or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["runtime"],
                    "value": tv.duration or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["genre"],
                    "value": tv.genre or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["network"],
                    "value": tv.studios or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["tv"]["reply"]["fields"]["watch"],
                    "value": tv.watch_on(region) or "-",
                    "inline": True,
                },
            ],
        }

    @staticmethod
    def from_person(person: Person, quotes: Language) -> dict:
        """Convert a `entities.Person` to a `discord.Embed` dict data."""
        return {
            "title": person.name,
            "description": person.description,
            "color": Color.bot,
            "url": person.url,
            "thumbnail": {"url": person.image} if person.image else {},
            "fields": [
                {
                    "name": quotes.commands["person"]["reply"]["fields"]["birthday"],
                    "value": person.date_birth.strftime(quotes.datetime_format) if person.date_birth else "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["person"]["reply"]["fields"]["deathday"],
                    "value": person.date_death.strftime(quotes.datetime_format) if person.date_death else "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["person"]["reply"]["fields"]["born"],
                    "value": person.place_of_birth or "-",
                    "inline": True,
                },
                {
                    "name": quotes.commands["person"]["reply"]["fields"]["know_for"],
                    "value": person.jobs or "-",
                    "inline": True,
                },
            ],
        }
