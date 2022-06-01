# -*- coding: utf-8 -*-
import asyncio
import random

import disnake
from disnake.ext import commands

from pypoca.config import COLOR
from pypoca.database import Server
from pypoca.exceptions import NoResults
from pypoca.services import tmdb, trakt
from pypoca.ext import ALL, DEFAULT, DEFAULT_LANGUAGE, DEFAULT_REGION, Choice, Movie, Option, Show


class Game:
    def __init__(self, inter: disnake.ApplicationCommandInteraction, *, category: str = None, ephemeral: bool = False) -> None:
        self.inter = inter
        self.ephemeral = ephemeral
        self.category = category
        self.selected = False
        self.movie = None
        self.movies = []
        self.options = []
        self.members = {}
        self.images = []
        self.embed = None
        self.view = None

        self.server = Server.get_or_create(
            id=self.inter.guild.id,
            data={"language": DEFAULT_LANGUAGE, "region": DEFAULT_REGION, "frame_record": 0, "higher_record": 0}
        )
        self.language = self.server.language or DEFAULT_LANGUAGE
        self.region = self.server.region or DEFAULT_REGION
        self.locale = ALL[self.language]

    @property
    def record(self) -> int:
        raise NotImplementedError()

    @property
    def score(self) -> int:
        if self.members:
            return sum(self.members.values())
        return 0

    def is_correct(self, value: str) -> bool:
        raise NotImplementedError()

    async def on_start(self) -> None:
        raise NotImplementedError()

    async def on_correct(self, inter: disnake.MessageInteraction) -> None:
        raise NotImplementedError()

    async def on_wrong(self, inter: disnake.MessageInteraction) -> None:
        raise NotImplementedError()

    async def on_select(self, inter: disnake.MessageInteraction, *, value: str) -> None:
        self.selected = True
        self.view.on_select(inter, value=value)
        await inter.response.edit_message(view=self.view)
        await asyncio.sleep(0.5)
        self.selected = False
        if self.is_correct(value):
            self.members[inter.author.mention] = self.members.get(inter.author.mention, 0) + 1
            await self.on_correct(inter)
            self.embed.on_correct()
            self.view.on_correct()
            embeds = [disnake.Embed()] * len(self.images)
            embeds[0] = self.embed
            for embed, image in zip(embeds, self.images):
                embed.url = self.images[0]
                embed.set_image(url=image)
            await inter.edit_original_message(embeds=embeds, view=self.view)
        else:
            await self.on_wrong(inter)
            self.embed.on_wrong()
            await inter.edit_original_message(embed=self.embed, view=None)

    async def start(self) -> None:
        await self.on_start()
        self.embed.on_start()
        self.view.on_start()
        embeds = [disnake.Embed()] * len(self.images)
        embeds[0] = self.embed
        for embed, image in zip(embeds, self.images):
            embed.url = self.images[0]
            embed.set_image(url=image)
        await self.inter.send(embeds=embeds, view=self.view, ephemeral=self.ephemeral)


class HigherLower(Game):
    def __init__(self, inter: disnake.ApplicationCommandInteraction, *, category: str, ephemeral: bool = False) -> None:
        super().__init__(inter, category=category, ephemeral=ephemeral)
        self.embed = GameEmbed(game=self, title=self.locale["COMMAND_GAME_HIGHER_REPLY"].format(category=self.locale[f"OPTION_HIGHER_CHOICE_{category.upper()}"]))
        self.view = GameButtons(game=self)

    @property
    def record(self) -> int:
        return self.server.higher_record or 0

    async def get_movie(self) -> Movie:
        while True:
            response = await tmdb.Movies(language=self.language, region=self.region).random()
            movie = Movie(response)
            if movie.image and getattr(movie, self.category) and movie not in self.movies:
                return movie

    def is_correct(self, value: str) -> bool:
        if self.movies[0].title[:25] == value:
            return getattr(self.movies[0], self.category) >= getattr(self.movies[1], self.category)
        if self.movies[1].title[:25] == value:
            return getattr(self.movies[0], self.category) <= getattr(self.movies[1], self.category)

    async def on_start(self) -> None:
        self.movies = [await self.get_movie(), await self.get_movie()]
        self.movie = self.movies[0]
        self.images = [movie.poster for movie in self.movies]
        self.options = [movie.title for movie in self.movies]

    async def on_correct(self, inter: disnake.MessageInteraction = None) -> None:
        self.movies = [self.movies[1], await self.get_movie()]
        self.movie = self.movies[0]
        self.images = [movie.poster for movie in self.movies]
        self.options = [movie.title for movie in self.movies]

    async def on_wrong(self, inter: disnake.MessageInteraction) -> None:
        if self.score > self.record:
            Server.update_by_id(inter.guild.id, data={"higher_record": self.score})


class FramedGame(Game):
    def __init__(self, inter: disnake.ApplicationCommandInteraction, *, ephemeral: bool = False) -> None:
        super().__init__(inter, ephemeral=ephemeral)
        self.embed = GameEmbed(game=self, title=self.locale["COMMAND_GAME_FRAME_REPLY"])
        self.view = GameSelect(game=self)

    @property
    def record(self) -> int:
        return self.server.frame_record or 0

    async def get_movie(self) -> Movie:
        while True:
            response = await tmdb.Movies(language=self.language, region=self.region).random(
                append="images,similar"
            )
            movie = Movie(response)
            if movie.backdrops:
                return movie

    def get_movies(self, *, movie: Movie) -> list[Movie]:
        movies = [Movie(choice) for choice in random.sample(movie.similar, k=4)] + [movie]
        random.shuffle(movies)
        return movies

    def is_correct(self, value: str) -> bool:
        return self.movie.title_and_year == value

    async def on_start(self) -> None:
        self.movie = await self.get_movie()
        self.movies = self.get_movies(movie=self.movie)
        self.images = [random.choice(self.movie.backdrops)]
        self.options = [movie.title_and_year for movie in self.movies]

    async def on_correct(self, inter: disnake.MessageInteraction = None) -> None:
        self.movie = await self.get_movie()
        self.movies = self.get_movies(movie=self.movie)
        self.images = [random.choice(self.movie.backdrops)]
        self.options = [movie.title_and_year for movie in self.movies]

    async def on_wrong(self, inter: disnake.MessageInteraction) -> None:
        if self.score > self.record:
            Server.update_by_id(inter.guild.id, data={"frame_record": self.score})


class GameDropdown(disnake.ui.Select):
    def __init__(self, game: Game) -> None:
        self.game = game
        super().__init__()

    async def callback(self, inter: disnake.MessageInteraction) -> None:
        await self.game.on_select(inter, value=self.values[0])


class GameSelect(disnake.ui.View):
    def __init__(self, game: Game) -> None:
        self.game = game
        super().__init__(timeout=None)
        self.add_item(GameDropdown(game))

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        return self.game.selected is False

    def on_start(self) -> None:
        for dropdown in self.children:
            dropdown.disabled = False
            dropdown.placeholder = self.game.locale["PLACEHOLDER"]
            dropdown.options = [disnake.SelectOption(label=option) for option in self.game.options]

    def on_correct(self) -> None:
        for dropdown in self.children:
            dropdown.disabled = False
            dropdown.placeholder = self.game.locale["PLACEHOLDER"]
            dropdown.options = [disnake.SelectOption(label=option) for option in self.game.options]

    def on_wrong(self) -> None:
        self.clear_items()

    def on_select(self, inter: disnake.MessageInteraction, *, value: str) -> None:
        for dropdown in self.children:
            dropdown.disabled = True
            dropdown.placeholder = value


class GameButton(disnake.ui.Button):
    def __init__(self, game: Game) -> None:
        self.game = game
        super().__init__()

    async def callback(self, inter: disnake.MessageInteraction) -> None:
        await self.game.on_select(inter, value=self.label)


class GameButtons(disnake.ui.View):
    def __init__(self, game: Game, *, num_buttons: int = 2) -> None:
        self.game = game
        super().__init__(timeout=None)
        for _ in range(num_buttons):
            self.add_item(GameButton(game))

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        return self.game.selected is False

    def on_start(self) -> None:
        for button, option in zip(self.children, self.game.options):
            button.disabled = False
            button.label = option[:25]

    def on_correct(self) -> None:
        for button, option in zip(self.children, self.game.options):
            button.disabled = False
            button.label = option[:25]

    def on_wrong(self) -> None:
        self.clear_items()

    def on_select(self, inter: disnake.MessageInteraction, *, value: str) -> None:
        for button in self.children:
            button.disabled = True


class GameEmbed(disnake.Embed):
    def __init__(self, game: Game, *, title: str) -> None:
        self.game = game
        super().__init__(title=title, color=COLOR)

    def on_start(self) -> None:
        self.add_field(self.game.locale["COMMAND_GAME_FIELD_SCORE"], 0, inline=True)
        self.add_field(self.game.locale["COMMAND_GAME_FIELD_RECORD"], self.game.record or "-", inline=True)

    def on_correct(self) -> None:
        self.clear_fields()
        self.add_field(self.game.locale["COMMAND_GAME_FIELD_SCORE"], self.game.score, inline=True)
        self.add_field(self.game.locale["COMMAND_GAME_FIELD_RECORD"], self.game.record or "-", inline=True)

    def on_wrong(self) -> None:
        self.set_image(url=disnake.embeds.EmptyEmbed)
        self.title = self.game.locale["COMMAND_GAME_END"]
        self.description = "\n".join(
            [
                f'{emoji} {member_score[0]} (**{member_score[1]}** {self.game.locale["COMMAND_GAME_POINTS"]})'
                for member_score, emoji in zip(sorted(self.game.members.items(), key=lambda x: x[1], reverse=True)[:5], "🏆🥈🥉🏅🏅")
            ]
        )

    def on_select(self, inter: disnake.MessageInteraction, *, value: str) -> None:
        pass


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="game", description=DEFAULT["COMMAND_GAME_DESC"])
    async def slash_game(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.defer()

    @slash_game.sub_command(name="framed", description=DEFAULT["COMMAND_GAME_FRAME_DESC"])
    async def slash_framed(self, inter: disnake.ApplicationCommandInteraction, hide: Choice.boolean = Option.hide) -> None:
        await FramedGame(inter, ephemeral=hide).start()

    @slash_game.sub_command(name="higher", description=DEFAULT["COMMAND_GAME_HIGHER_DESC"])
    async def slash_higher(
        self, inter: disnake.ApplicationCommandInteraction, category: Choice.higher = Option.higher, hide: Choice.boolean = Option.hide
    ) -> None:
        await HigherLower(inter, category=category, ephemeral=hide).start()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Games(bot))
