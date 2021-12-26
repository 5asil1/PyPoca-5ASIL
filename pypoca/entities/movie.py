# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

__all__ = "Movie"


@dataclass
class Movie:
    id: int
    original_name: str
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    image_path: Optional[str] = None
    date: Optional[datetime] = None
    status: Optional[str] = None
    runtime: Optional[int] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    imdb_id: Optional[str] = None
    trakt_id: Optional[str] = None
    youtube_id: Optional[str] = None
    genres: list = field(default_factory=list)
    companies: list = field(default_factory=list)
    crew: list = field(default_factory=list)
    cast: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    providers: list = field(default_factory=list)

    @classmethod
    def from_tmdb(cls, result: dict) -> Movie:
        """Convert a `dict` data movie result to a `pypoca.entities.Movie`."""
        id = result["id"]
        name = result.get("title")
        original_name = result.get("original_title")
        description = result.get("overview")
        url = result.get("homepage")
        image_path = result.get("backdrop_path")
        release_date = result.get("release_date")
        date = datetime.strptime(release_date, "%Y-%m-%d") if release_date else None
        runtime = result.get("runtime")
        rating = result.get("vote_average")
        votes = result.get("vote_count")
        status = result.get("status")
        external_ids = result.get("external_ids")
        trakt_id = external_ids.get("trakt_id") if external_ids else None
        imdb_id = external_ids.get("imdb_id") if external_ids else None
        youtube_id = (
            result["videos"]["results"][0]["key"] if result.get("videos") and result["videos"]["results"] else None
        )
        genres = [genre["name"] for genre in result.get("genres") or []]
        companies = [company["name"] for company in result.get("production_companies") or []]
        crew = result["credits"]["crew"] if result.get("credits") else []
        cast = result["credits"]["cast"] if result.get("credits") else []
        recommendations = result["recommendations"]["results"] if result.get("recommendations") else []
        providers = result["watch/providers"]["results"] if result.get("watch/providers") else []
        return cls(
            id=id,
            original_name=original_name,
            name=name,
            description=description,
            url=url,
            image_path=image_path,
            date=date,
            status=status,
            votes=votes,
            rating=rating,
            runtime=runtime,
            youtube_id=youtube_id,
            imdb_id=imdb_id,
            trakt_id=trakt_id,
            genres=genres,
            companies=companies,
            providers=providers,
            crew=crew,
            cast=cast,
            recommendations=recommendations,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} original_name={self.original_name}>"

    def __str__(self) -> str:
        return self.name_and_year

    @property
    def title(self) -> str:
        return self.name or self.original_name

    @property
    def name_and_year(self) -> str:
        return f"{self.title[:90]} ({self.date.year})" if self.date else self.title[:100]

    @property
    def duration(self) -> Optional[str]:
        if not self.runtime:
            return None
        hours, minutes = divmod(int(self.runtime), 60)
        duration = ""
        if hours != 0:
            duration += f"{hours}h "
        if minutes != 0:
            duration += f"{minutes}min"
        return duration

    @property
    def image(self) -> Optional[str]:
        return f"https://image.tmdb.org/t/p/w1280/{self.image_path}" if self.image_path else None

    @property
    def rating_and_votes(self) -> Optional[str]:
        return f"{self.rating} ({self.votes})" if self.rating else None

    @property
    def trailer(self) -> str:
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def imdb(self) -> str:
        return f"https://www.imdb.com/title/{self.imdb_id}"

    @property
    def directors(self) -> Optional[str]:
        directors = [person["name"] for person in self.crew if person["job"] == "Director"]
        return ", ".join(directors) if directors else None

    @property
    def genre(self) -> Optional[str]:
        return ", ".join(self.genres) if self.genres else None

    @property
    def studios(self) -> Optional[str]:
        return ", ".join(self.companies) if self.companies else None

    def watch_on(self, region: str) -> Optional[str]:
        """Get all the watch providers for the specified region."""
        if not self.providers.get(region) or not self.providers[region].get("flatrate"):
            return None
        providers = [provider["provider_name"] for provider in self.providers[region]["flatrate"]]
        if self.trakt_id:
            trakt_url = "https://trakt.tv/watchnow/movie"
            providers = [
                f"[{provider}]({trakt_url}/{self.trakt_id}/1/{region}/{provider.replace(' ', '_').lower()})"
                for provider in providers
            ]
        return ", ".join(providers) if providers else None
