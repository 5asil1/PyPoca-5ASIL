# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

__all__ = "TV"


@dataclass
class TV:
    id: int
    original_name: str
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    image_path: Optional[str] = None
    date: Optional[datetime] = None
    date_end: Optional[datetime] = None
    status: Optional[str] = None
    episodes: Optional[int] = None
    seasons: Optional[int] = None
    runtime_per_episode: Optional[int] = None
    runtime: Optional[int] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    imdb_id: Optional[str] = None
    trakt_id: Optional[str] = None
    youtube_id: Optional[str] = None
    genres: list = field(default_factory=list)
    networks: list = field(default_factory=list)
    crew: list = field(default_factory=list)
    cast: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    providers: list = field(default_factory=list)
    created_by: list = field(default_factory=list)

    @classmethod
    def from_tmdb(cls, result: dict) -> TV:
        """Convert a `dict` data TV show result to a `pypoca.entities.TV`."""
        id = result["id"]
        name = result.get("name")
        original_name = result.get("original_name")
        description = result.get("overview")
        url = result.get("homepage")
        image_path = result.get("backdrop_path")
        first_air_date = result.get("first_air_date")
        last_air_date = result.get("last_air_date")
        date = datetime.strptime(first_air_date, "%Y-%m-%d") if first_air_date else None
        date_end = datetime.strptime(last_air_date, "%Y-%m-%d") if last_air_date else None
        episodes = result.get("number_of_episodes", 0)
        seasons = result.get("number_of_seasons", 0)
        runtime_per_episode = (
            sum(result["episode_run_time"]) / len(result["episode_run_time"]) if result.get("episode_run_time") else 0
        )
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
        networks = [network["name"] for network in result.get("networks") or []]
        crew = result["credits"]["crew"] if result.get("credits") else []
        cast = result["credits"]["cast"] if result.get("credits") else []
        recommendations = result["recommendations"]["results"] if result.get("recommendations") else []
        providers = result["watch/providers"]["results"] if result.get("watch/providers") else []
        created_by = result.get("created_by")
        return cls(
            id=id,
            original_name=original_name,
            name=name,
            description=description,
            url=url,
            image_path=image_path,
            date=date,
            date_end=date_end,
            status=status,
            episodes=episodes,
            seasons=seasons,
            runtime_per_episode=runtime_per_episode,
            runtime=runtime,
            rating=rating,
            votes=votes,
            imdb_id=imdb_id,
            trakt_id=trakt_id,
            youtube_id=youtube_id,
            genres=genres,
            networks=networks,
            crew=crew,
            cast=cast,
            recommendations=recommendations,
            providers=providers,
            created_by=created_by,
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
    def duration_episode(self) -> Optional[str]:
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
    def duration_total(self) -> Optional[str]:
        if not self.runtime_per_episode or not self.episodes:
            return None
        hours, minutes = divmod(int(self.runtime_per_episode * self.episodes), 60)
        days, hours = divmod(int(hours), 24)
        duration = ""
        if days != 0:
            duration += f"{days}d "
        if hours != 0:
            duration += f"{hours}h "
        if minutes != 0:
            duration += f"{minutes}min"
        return duration

    @property
    def duration(self) -> Optional[str]:
        if not self.duration_episode and not self.duration_total:
            return None
        if not self.duration_total:
            return self.duration_episode
        return f"{self.duration_episode} ({self.duration_total} total)"

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
        directors = [person["name"] for person in self.created_by]
        return ", ".join(directors) if directors else None

    @property
    def genre(self) -> Optional[str]:
        return ", ".join(self.genres) if self.genres else None

    @property
    def studios(self) -> Optional[str]:
        return ", ".join(self.networks) if self.networks else None

    def watch_on(self, region: str) -> Optional[str]:
        """Get all the watch providers for the specified region."""
        if not self.providers.get(region) or not self.providers[region].get("flatrate"):
            return None
        providers = [provider["provider_name"] for provider in self.providers[region]["flatrate"]]
        if self.trakt_id:
            trakt_url = "https://trakt.tv/watchnow/show"
            providers = [
                f"[{provider}]({trakt_url}/{self.trakt_id}/1/{region}/{provider.replace(' ', '_').lower()})"
                for provider in providers
            ]
        return ", ".join(providers) if providers else None
