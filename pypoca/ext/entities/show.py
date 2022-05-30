# -*- coding: utf-8 -*-
from datetime import date, datetime


class Show(dict):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.backdrop_path = data.get("backdrop_path")
        self.created_by = data.get("created_by") or []
        self.episode_run_time = data.get("episode_run_time") or []
        self.first_air_date = data.get("first_air_date")
        self._genres = data.get("genres") or []
        self.homepage = data.get("homepage", "")
        self.id = data.get("id")
        self.in_production = data.get("in_production")
        self.languages = data.get("languages") or []
        self.last_air_date = data.get("last_air_date")
        self.last_episode_to_air = data.get("last_episode_to_air")
        self.name = data.get("name", "")
        self.next_episode_to_air = data.get("next_episode_to_air")
        self.networks = data.get("networks") or []
        self.number_of_episodes = data.get("number_of_episodes") or 0
        self.number_of_seasons = data.get("number_of_seasons") or 0
        self.origin_country = data.get("origin_country") or []
        self.original_language = data.get("original_language")
        self.original_name = data.get("original_name", "")
        self.overview = data.get("overview")
        self.popularity = data.get("popularity")
        self.poster_path = data.get("poster_path")
        self.production_companies = data.get("production_companies") or []
        self.production_countries = data.get("production_countries") or []
        self.seasons = data.get("seasons") or []
        self.spoken_languages = data.get("spoken_languages") or []
        self.status = data.get("status")
        self.tagline = data.get("tagline")
        self.type = data.get("type")
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
        return f"{self.title[:90]} ({self.first_date.year})" if self.first_date else self.title[:100]

    @property
    def first_date(self) -> date:
        if self.first_air_date:
            return datetime.strptime(self.first_air_date, "%Y-%m-%d").date()

    @property
    def last_date(self) -> date:
        if self.last_air_date:
            return datetime.strptime(self.last_air_date, "%Y-%m-%d").date()

    @property
    def image(self) -> str:
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280/{self.backdrop_path}"

    @property
    def poster(self) -> str:
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280/{self.poster_path}"

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
    def runtime_per_episode(self) -> int:
        return int(sum(self.episode_run_time) / len(self.episode_run_time)) if self.episode_run_time else 0

    @property
    def duration_per_episode(self) -> str:
        if self.runtime_per_episode:
            hours, minutes = divmod(self.runtime_per_episode, 60)
            duration = ""
            if hours != 0:
                duration += f"{int(hours)}h "
            if minutes != 0:
                duration += f"{int(minutes)}min"
            return duration

    @property
    def duration_total(self) -> str:
        if self.runtime_per_episode and self.number_of_episodes:
            hours, minutes = divmod(self.runtime_per_episode * self.number_of_episodes, 60)
            duration = ""
            if hours != 0:
                duration += f"{int(hours)}h "
            if minutes != 0:
                duration += f"{int(minutes)}min"
            return duration

    @property
    def duration(self) -> str:
        if self.duration_per_episode and self.duration_total:
            return f"{self.duration_per_episode} ({self.duration_total} total)"
        if self.duration_per_episode:
            return self.duration_per_episode

    @property
    def rating_and_votes(self) -> str:
        if self.vote_average and self.vote_count:
            return f"{self.vote_average} ({self.vote_count})"

    @property
    def directors(self) -> list[str]:
        return [person["name"] for person in self.created_by]

    @property
    def genres(self) -> list[str]:
        return [genre["name"] for genre in self._genres]

    @property
    def studios(self) -> list[str]:
        return [network["name"] for network in self.networks]

    def watch_on(self, region: str) -> list[str]:
        if self.watch_providers.get("results") and self.watch_providers["results"].get(region) and self.watch_providers["results"][region].get("flatrate"):
            providers = [provider["provider_name"] for provider in self.watch_providers["results"][region]["flatrate"]]
            if self.trakt_id:
                trakt_url = "https://trakt.tv/watchnow/show"
                providers = [
                    f"[{provider}]({trakt_url}/{self.trakt_id}/1/{region}/{provider.replace(' ', '_').lower()})"
                    for provider in providers
                ]
            return providers
        return []
