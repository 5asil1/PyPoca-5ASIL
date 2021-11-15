# -*- coding: utf-8 -*-

__all__ = (
    "DATETIME_STR",
    "OptionDescription",
    "Placeholder",
    "EventReply",
    "CommandDescription",
    "CommandReply",
    "Language",
    "Region",
    "Genre",
)

DATETIME_STR = "%Y/%m/%d"


class Reply:
    """Basic reply model."""

    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class OptionDescription:
    """All available option descriptions with the respectives regionalized name."""

    query = "A text query to search"
    page = "Specify which page to query"
    language = "A ISO 639-1 value to display translated data"
    region = "A ISO 3166-1 code to filter release dates"
    nsfw = "Choose whether to inlcude adult (pornography) content in the results"
    sort_by = "Choose from one of the many available sort options"
    year = "Only include results that have a release date that is equal to the specified value"
    min_year = "Only include results that have a release date that is greater or equal to the specified value"
    max_year = "Only include results that have a release date that is less than or equal to the specified value"
    min_votes = "Only include results that have a vote count that is greater or equal to the specified value"
    max_votes = "Only include results that have a vote count that is less than or equal to the specified value"
    min_rating = "Only include results that have a rating that is greater or equal to the specified value"
    max_rating = "Only include results that have a rating that is less than or equal to the specified value"
    min_runtime = "Only include results that have a runtime that is greater or equal to a value"
    max_runtime = "Only include results that have a runtime that is less than or equal to a value"
    interval = "View the trending list for the day or week"
    hide = "The command response will only be visible to you"
    service = "Filter the results by specific streaming service or channel"


class Placeholder:
    """All available placeholders with the respectives regionalized name."""

    menu = "Select one of the options..."


class EventReply:
    """All available event replies with the respectives regionalized name."""

    cooldown = Reply(
        title="Command `{command_name}` is on cooldown",
        description="You are on cooldown. Try again in {time:.2f} seconds",
    )
    not_found = Reply(
        title="No results found",
        description="Could not find any match for these specifications",
    )
    exception = Reply(
        title="An unexpected error occurred with `{command_name}` command",
        description="Error: {error}",
    )


class CommandDescription:
    """All available command descriptions with the respectives regionalized name."""

    ping = "Get PyPoca's latency"
    help = "Shows PyPoca's help menu"
    movie = "All about movies: find, discover and get information"
    person = "All about people: find, discover and get information"
    tv = "All about TV shows: find, discover and get information"
    discover_movie = "Discover movies by different types of data"
    popular_movie = "Get the current popular movies"
    search_movie = "Search for a movie"
    top_movie = "Get the top rated movies"
    trending_movie = "Get the trending movies"
    upcoming_movie = "Get the upcoming movies in theatres"


class CommandReply:
    """All available command replies with the respectives regionalized name."""

    ping = Reply(title="Pong!", description="Latency: {latency}ms")
    help = Reply(
        title="Available commands",
        description="Millions of movies, TV shows and people to discover. Explore now!",
    )


class Language:
    """All available languages with the respectives regionalized name."""

    en_US = "English"
    pt_BR = "Portuguese"


class Region:
    """All available regions with the respectives regionalized name."""

    BR = "Brazil"
    US = "United States"


class Genre:
    """All available genres with the respectives regionalized name."""

    action = "Action"
    action_and_adventure = "Action & Adventure"
    adventure = "Adventure"
    animation = "Animation"
    comedy = "Comedy"
    crime = "Crime"
    documentary = "Documentary"
    drama = "Drama"
    family = "Family"
    fantasy = "Fantasy"
    history = "History"
    horror = "Horror"
    kids = "Kids"
    music = "Music"
    mystery = "Mystery"
    news = "News"
    reality = "Reality"
    romance = "Romance"
    soap = "Soap"
    syfy = "Science Fiction"
    syfy_and_fantasy = "Sci-Fi & Fantasy"
    talk = "Talk"
    tv = "TV Movie"
    thriller = "Thriller"
    war = "War"
    war_and_politics = "War & Politics"
    western = "Western"
