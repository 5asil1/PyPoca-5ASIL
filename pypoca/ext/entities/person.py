# -*- coding: utf-8 -*-
from datetime import date, datetime


class Person(dict):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.adult = data.get("adult")
        self.also_known_as = data.get("also_known_as")
        self.biography = data.get("biography", "")
        self._birthday = data.get("birthday")
        self._deathday = data.get("deathday")
        self.gender = data.get("gender")
        self.homepage = data.get("homepage")
        self.id = data.get("id")
        self._known_for = data.get("known_for")
        self.known_for_department = data.get("known_for_department")
        self.name = data.get("name", "")
        self.place_of_birth = data.get("place_of_birth")
        self.popularity = data.get("popularity")
        self.profile_path = data.get("profile_path")

        self.external_ids = data.get("external_ids") or {}
        self.credits = data.get("combined_credits") or {}

    @property
    def birthday(self) -> date:
        if self._birthday:
            return datetime.strptime(self._birthday, "%Y-%m-%d").date()

    @property
    def deathday(self) -> date:
        if self._deathday:
            return datetime.strptime(self._deathday, "%Y-%m-%d").date()

    @property
    def image(self) -> str:
        if self.profile_path:
            return f"https://image.tmdb.org/t/p/w1280/{self.profile_path}"

    @property
    def imdb_id(self) -> str:
        if self.external_ids.get("imdb_id"):
            return self.external_ids.get("imdb_id")

    @property
    def instagram_id(self) -> str:
        if self.external_ids.get("instagram_id"):
            return self.external_ids.get("instagram_id")

    @property
    def twitter_id(self) -> str:
        if self.external_ids.get("twitter_id"):
            return self.external_ids.get("twitter_id")

    @property
    def imdb(self) -> str:
        return f"https://www.imdb.com/name/{self.imdb_id}"

    @property
    def instagram(self) -> str:
        return f"https://www.instagram.com/{self.instagram_id}"

    @property
    def twitter(self) -> str:
        return f"https://www.twitter.com/{self.twitter_id}"

    @property
    def cast(self) -> list[dict]:
        return self.credits.get("cast") or []

    @property
    def cast_movies(self) -> list[dict]:
        return [cast for cast in self.cast if cast["media_type"] == "movie"]

    @property
    def cast_shows(self) -> list[dict]:
        return [cast for cast in self.cast if cast["media_type"] == "tv"]

    @property
    def crew(self) -> list[dict]:
        return self.credits.get("crew") or []

    @property
    def crew_movies(self) -> list[dict]:
        return [crew for crew in self.crew if crew["media_type"] == "movie"]

    @property
    def crew_shows(self) -> list[dict]:
        return [crew for crew in self.crew if crew["media_type"] == "tv"]

    @property
    def jobs(self) -> list[str]:
        jobs = self._known_for or (self.cast if self.known_for_department == "Acting" else self.crew)
        return [
            job.get("title") or job.get("name") or job.get("original_title") or job.get("original_name")
            for job in jobs
        ]
