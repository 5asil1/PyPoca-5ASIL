# -*- coding: utf-8 -*-
from aiotmdb import AsObj

from pypoca.adapters import movie, person, tv


class Adapter:
    def __init__(self, type: str) -> None:
        if type == "movie":
            self._embed = movie.embed
            self._option = movie.option
            self._buttons = movie.buttons
        elif type == "person":
            self._embed = person.embed
            self._option = person.option
            self._buttons = person.buttons
        elif type == "tv":
            self._embed = tv.embed
            self._option = tv.option
            self._buttons = tv.buttons
        else:
            raise ValueError(f"Adapter 'type' must be 'movie', 'person' or 'tv', not {type}")

    def embed(self, result: AsObj, region: str) -> dict:
        return self._embed(result, region)

    def option(self, result: AsObj) -> dict:
        return self._option(result)

    def buttons(self, result: AsObj) -> dict:
        return self._buttons(result)
