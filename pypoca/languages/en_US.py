# -*- coding: utf-8 -*-

__all__ = (
    "OptionsDescription",
    "Placeholders",
    "EventsResponse",
    "CommandsDescription",
    "CommandsResponse",
    "Languages",
    "Regions",
    "Genres",
)


class Response(object):
    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class OptionsDescription:
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


class Placeholders:
    menu = "Select one of the options..."


class EventsResponse:
    cooldown = Response(
        title="Command `{command_name}` is on cooldown",
        description="You are on cooldown. Try again in {time:.2f} seconds",
    )
    not_found = Response(
        title="No results found",
        description="Could not find any match for these specifications",
    )
    exception = Response(
        title="An unexpected error occurred with `{command_name}` command",
        description="Error: {error}",
    )


class CommandsDescription:
    ping = "Get PyPoca's latency"
    help = "Shows PyPoca's help menu"
    movie = "All about movies: find, discover and get information"
    person = "All about people: find, discover and get information"
    tv = "All about TV shows: find, discover and get information"


class CommandsResponse:
    ping = Response(title="Pong!", description="Latency: {latency}ms")
    help = Response(
        title="Available commands",
        description="Millions of movies, TV shows and people to discover. Explore now!",
    )


class Languages:
    en_US = "English"
    pt_BR = "Portuguese"


class Regions:
    BR = "Brazil"
    US = "United States"


class Genres:
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
