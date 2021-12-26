# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

__all__ = "Person"


@dataclass
class Person:
    id: int
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    image_path: Optional[str] = None
    date_birth: Optional[datetime] = None
    date_death: Optional[datetime] = None
    place_of_birth: Optional[str] = None
    imdb_id: Optional[str] = None
    instagram_id: Optional[str] = None
    twitter_id: Optional[str] = None
    character: Optional[str] = None
    job: Optional[str] = None
    known_for_department: Optional[str] = None
    known_for: list = field(default_factory=list)
    crew: list = field(default_factory=list)
    cast: list = field(default_factory=list)
    crew_movie: list = field(default_factory=list)
    cast_movie: list = field(default_factory=list)
    crew_tv: list = field(default_factory=list)
    cast_tv: list = field(default_factory=list)

    @classmethod
    def from_tmdb(cls, result: dict) -> Person:
        """Convert a `dict` data person result to a `dict` with Discord embed items."""
        id = result["id"]
        name = result.get("name")
        description = result.get("biography")
        url = result.get("homepage")
        image_path = result.get("profile_path")
        birthday = result.get("birthday")
        deathday = result.get("deathday")
        date_birth = datetime.strptime(birthday, "%Y-%m-%d") if birthday else None
        date_death = datetime.strptime(deathday, "%Y-%m-%d") if deathday else None
        place_of_birth = result.get("place_of_birth")
        external_ids = result.get("external_ids")
        imdb_id = external_ids.get("imdb_id") if external_ids else None
        instagram_id = external_ids.get("instagram_id") if external_ids else None
        twitter_id = external_ids.get("twitter_id") if external_ids else None
        character = result.get("character")
        job = result.get("job")
        known_for_department = result.get("known_for_department")
        known_for = result.get("known_for") or []
        crew = result["combined_credits"].get("crew") if result.get("combined_credits") else []
        cast = result["combined_credits"].get("cast") if result.get("combined_credits") else []
        crew_movie = result["movie_credits"].get("crew") if result.get("movie_credits") else []
        cast_movie = result["movie_credits"].get("cast") if result.get("movie_credits") else []
        crew_tv = result["tv_credits"].get("crew") if result.get("tv_credits") else []
        cast_tv = result["tv_credits"].get("cast") if result.get("tv_credits") else []
        return cls(
            id=id,
            name=name,
            description=description,
            url=url,
            image_path=image_path,
            date_birth=date_birth,
            date_death=date_death,
            place_of_birth=place_of_birth,
            imdb_id=imdb_id,
            instagram_id=instagram_id,
            twitter_id=twitter_id,
            character=character,
            job=job,
            known_for_department=known_for_department,
            known_for=known_for,
            crew=crew,
            cast=cast,
            crew_movie=crew_movie,
            cast_movie=cast_movie,
            crew_tv=crew_tv,
            cast_tv=cast_tv,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"

    def __str__(self) -> str:
        return self.name

    @property
    def image(self) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/w1280/{self.image_path}" if self.image_path else None

    @property
    def imdb(self) -> str:
        return f"https://www.imdb.com/title/{self.imdb_id}"

    @property
    def instagram(self) -> str:
        return f"https://www.instagram.com/{self.instagram_id}"

    @property
    def twitter(self) -> str:
        return f"https://www.twitter.com/{self.twitter_id}"

    @property
    def jobs(self) -> str:
        jobs = self.known_for or (self.cast if self.known_for_department == "Acting" else self.crew)
        jobs = [
            known_for.get("title") or known_for["original_title"]
            if known_for["media_type"] == "movie"
            else known_for.get("name") or known_for["original_name"]
            for known_for in jobs[:6]
        ]
        return ", ".join(jobs)
