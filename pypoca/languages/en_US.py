# -*- coding: utf-8 -*-

__all__ = (
    "DATETIME_STR",
    "Boolean",
    "CommandDescription",
    "CommandReply",
    "EventReply",
    "Genre",
    "Interval",
    "Language",
    "Option",
    "Placeholder",
    "Region",
    "Sort",
)

DATETIME_STR = "%Y/%m/%d"


class Object:
    """Basic object title-description model."""

    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class Option:
    """All available option descriptions with the respectives regionalized name."""

    query = Object(
        title="query",
        description="A text query to search",
    )
    page = Object(
        title="page",
        description="Specify which page to query",
    )
    language = Object(
        title="language",
        description="A ISO 639-1 value to display translated data",
    )
    region = Object(
        title="region",
        description="A ISO 3166-1 code to filter release dates",
    )
    nsfw = Object(
        title="adult",
        description="Choose whether to inlcude adult (pornography) content in the results",
    )
    sort_by = Object(
        title="sort-by",
        description="Choose from one of the many available sort options",
    )
    year = Object(
        title="year",
        description="Only include results that have a release date that is equal to the specified value",
    )
    min_year = Object(
        title="min-year",
        description="Only include results that have a release date that is greater or equal to the specified value",
    )
    max_year = Object(
        title="max-year",
        description="Only include results that have a release date that is less than or equal to the specified value",
    )
    min_votes = Object(
        title="min-votes",
        description="Only include results that have a vote count that is greater or equal to the specified value",
    )
    max_votes = Object(
        title="max-votes",
        description="Only include results that have a vote count that is less than or equal to the specified value",
    )
    min_rating = Object(
        title="min-rating",
        description="Only include results that have a rating that is greater or equal to the specified value",
    )
    max_rating = Object(
        title="max-rating",
        description="Only include results that have a rating that is less than or equal to the specified value",
    )
    min_runtime = Object(
        title="min-runtime",
        description="Only include results that have a runtime that is greater or equal to a value",
    )
    max_runtime = Object(
        title="max-runtime",
        description="Only include results that have a runtime that is less than or equal to a value",
    )
    interval = Object(
        title="interval",
        description="Choose between the trends of the day or the week",
    )
    hide = Object(
        title="hide",
        description="The command response will only be visible to you",
    )
    service = Object(
        title="service",
        description="Filter the results by specific streaming service or channel",
    )
    service = Object(
        title="genre",
        description="Filter the results by specific genre",
    )


class Placeholder:
    """All available placeholders with the respectives regionalized name."""

    menu = "Select one of the options..."


class EventReply:
    """All available event replies with the respectives regionalized name."""

    cooldown = Object(
        title="Command `{command_name}` is on cooldown",
        description="You are on cooldown. Try again in {time:.2f} seconds",
    )
    not_found = Object(
        title="No results found",
        description="Could not find any match for these specifications",
    )
    exception = Object(
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
    discover_tv = "Discover TV shows by different types of data"
    popular_movie = "Get the current popular movies"
    popular_person = "Get the current popular people"
    popular_tv = "Get the current popular TV shows"
    search_movie = "Search for a movie"
    search_person = "Search for people"
    search_tv = "Search for TV show"
    top_movie = "Get the top rated movies"
    top_tv = "Get the top rated TV shows"
    trending_movie = "Get the trending movies"
    trending_person = "Get the trending people"
    trending_tv = "Get the trending TV shows"
    upcoming_movie = "Get the upcoming movies in theatres"
    upcoming_tv = "Get the upcoming TV shows"


class CommandReply:
    """All available command replies with the respectives regionalized name."""

    ping = Object(title="Pong!", description="Latency: {latency}ms")
    help = Object(
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

    action = "action"
    action_and_adventure = "action & adventure"
    adventure = "adventure"
    animation = "animation"
    comedy = "comedy"
    crime = "crime"
    documentary = "documentary"
    drama = "drama"
    family = "family"
    fantasy = "fantasy"
    history = "history"
    horror = "horror"
    kids = "kids"
    music = "music"
    mystery = "mystery"
    news = "news"
    reality = "reality"
    romance = "romance"
    soap = "soap"
    syfy = "science fiction"
    syfy_and_fantasy = "sci-fi & fantasy"
    talk = "talk"
    tv = "TV movie"
    thriller = "thriller"
    war = "war"
    war_and_politics = "war & politics"
    western = "western"


class Sort:
    """All available orderings with the respectives regionalized name."""

    popularity = "popularity"
    year = "year"
    rating = "rating"
    title = "title"
    votes = "votes"


class Interval:
    """All available intervals with the respectives regionalized name."""

    day = "day"
    week = "week"


class Boolean:
    """True and False boolean options with the respectives regionalized name."""

    true = "yes"
    false = "no"
