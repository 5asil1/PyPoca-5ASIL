# -*- coding: utf-8 -*-
from datetime import datetime


class Movie(dict):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.adult = data.get("adult")
        self.backdrop_path = data.get("backdrop_path")
        self.belongs_to_collection = data.get("belongs_to_collection")
        self.budget = data.get("budget")
        self._genres = data.get("genres") or []
        self.homepage = data.get("homepage")
        self.id = data.get("id")
        self.name = data.get("title", "")
        self.original_language = data.get("original_language")
        self.original_name = data.get("original_title", "")
        self.overview = data.get("overview")
        self.popularity = data.get("popularity")
        self.poster_path = data.get("poster_path")
        self.production_companies = data.get("production_companies") or []
        self.production_countries = data.get("production_countries") or []
        self._release_date = data.get("release_date")
        self.revenue = data.get("revenue")
        self.runtime = data.get("runtime")
        self.spoken_languages = data.get("spoken_languages") or []
        self.status = data.get("status")
        self.tagline = data.get("tagline")
        self.video = data.get("video")
        self.vote_average = data.get("vote_average")
        self.vote_count = data.get("vote_count")

        self.alternative_titles = data.get("alternative_titles") or {}
        self.credits = data.get("credits") or {}
        self.external_ids = data.get("external_ids") or {}
        self.images = data.get("images") or {}
        self.recommendations = data["recommendations"]["results"] if data.get("recommendations") else []
        self.similar = data["similar"]["results"] if data.get("similar") else []
        self.videos = data.get("videos")
        self.watch_providers = data.get("watch/providers")

    @property
    def title(self) -> str:
        return self.name or self.original_name

    @property
    def title_and_year(self) -> str:
        return f"{self.title[:90]} ({self.release_date.year})" if self.release_date else self.title[:100]

    @property
    def release_date(self) -> datetime:
        if self._release_date:
            return datetime.strptime(self._release_date, "%Y-%m-%d")

    @property
    def image(self) -> str:
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280/{self.backdrop_path}"

    @property
    def imdb_id(self) -> str:
        if self.external_ids.get("imdb_id"):
            return self.external_ids.get("imdb_id")

    @property
    def youtube_id(self) -> str:
        if self.videos and self.videos["results"]:
            return self.videos["results"][0]["key"]

    @property
    def trakt_id(self) -> str:
        if self.external_ids.get("trakt_id"):
            return self.external_ids.get("trakt_id")

    @property
    def imdb(self) -> str:
        return f"https://www.imdb.com/title/{self.imdb_id}"

    @property
    def youtube(self) -> str:
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def cast(self) -> dict:
        return self.credits.get("cast") or []

    @property
    def crew(self) -> dict:
        return self.credits.get("crew") or []

    @property
    def duration(self) -> str:
        if self.runtime:
            hours, minutes = divmod(self.runtime, 60)
            duration = ""
            if hours != 0:
                duration += f"{int(hours)}h "
            if minutes != 0:
                duration += f"{int(minutes)}min"
            return duration

    @property
    def rating_and_votes(self) -> str:
        if self.vote_average and self.vote_count:
            return f"{self.vote_average} ({self.vote_count})"

    @property
    def directors(self) -> list[str]:
        return [person["name"] for person in self.crew if person["job"] == "Director"]

    @property
    def genres(self) -> list[str]:
        return [genre["name"] for genre in self._genres]

    @property
    def studios(self) -> list[str]:
        return [company["name"] for company in self.production_companies]

    def watch_on(self, region: str) -> list[str]:
        if self.watch_providers.get("results") and self.watch_providers["results"].get(region) and self.watch_providers["results"][region].get("flatrate"):
            providers = [provider["provider_name"] for provider in self.watch_providers["results"][region]["flatrate"]]
            if self.trakt_id:
                trakt_url = "https://trakt.tv/watchnow/movie"
                providers = [
                    f"[{provider}]({trakt_url}/{self.trakt_id}/1/{region}/{provider.replace(' ', '_').lower()})"
                    for provider in providers
                ]
            return providers
        return []
