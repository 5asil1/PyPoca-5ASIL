# -*- coding: utf-8 -*-
import random

import disnake
from disnake.ext import commands

from pypoca.config import COLOR
from pypoca.database import Server
from pypoca.exceptions import NoResults
from pypoca.services import tmdb, trakt
from pypoca.ext import ALL, DEFAULT, DEFAULT_LANGUAGE, DEFAULT_REGION, Choice, Movie, Option, Show


class FramedGame:
    def __init__(self, inter: disnake.ApplicationCommandInteraction, *, ephemeral: bool = False) -> None:
        self.inter = inter
        self.members = {}
        self.ephemeral = ephemeral

        self.server = Server.get_or_create(id=self.inter.guild.id, data={"language": DEFAULT_LANGUAGE, "region": DEFAULT_REGION, "frame_record": 0})
        self.language = self.server.language or DEFAULT_LANGUAGE
        self.region = self.server.region or DEFAULT_REGION
        self.record = self.server.frame_record or 0
        self.locale = ALL[self.language]

        self.embed = FramedEmbed(game=self)
        self.view = FramedSelect(game=self)

    @property
    def score(self) -> int:
        if self.members:
            return sum(self.members.values())
        return 0

    @property
    def top_scorer(self) -> str:
        if self.members:
            return max(self.members, key=self.members.get)
        return None

    async def start(self) -> None:
        await self.update_frame()
        await self.inter.send(embed=self.embed, view=self.view, ephemeral=self.ephemeral)

    async def update(self, inter: disnake.MessageInteraction) -> None:
        self.members[inter.author.mention] = self.members.get(inter.author.mention, 0) + 1
        await self.update_frame()
        await inter.response.edit_message(embed=self.embed, view=self.view)

    async def stop(self, inter: disnake.MessageInteraction) -> None:
        if self.score > self.record:
            Server.update_by_id(inter.guild.id, data={"frame_record": self.score})
        self.embed.stop()
        await inter.response.edit_message(embed=self.embed, view=None)

    async def update_frame(self) -> None:
        self.movie = await self.get_random_movie()
        self.movies = self.get_similar_movies(movie=self.movie)
        self.embed.update()
        self.view.children[0].options = [
            disnake.SelectOption(
                label=movie.title_and_year,
                value=movie.id,
            )
            for movie in self.movies
        ]

    async def get_random_movie(self) -> Movie:
        while True:
            response = await tmdb.Movies(language=self.language, region=self.region).random(
                append="images,similar"
            )
            movie = Movie(response)
            if movie.backdrops:
                return movie

    def get_similar_movies(self, *, movie: Movie, include_self: bool = True, shuffle: bool = True, num: int = 4) -> list[Movie]:
        choices = random.sample(movie.similar, k=num)
        movies = [Movie(choice) for choice in choices]
        if include_self:
            movies.append(movie)
        if shuffle:
            random.shuffle(movies)
        return movies


class FramedDropdown(disnake.ui.Select):
    def __init__(self, game: FramedGame) -> None:
        self.game = game
        super().__init__(placeholder=self.game.locale["PLACEHOLDER"])

    async def callback(self, inter: disnake.MessageInteraction) -> None:
        if self.game.movie.id == int(self.values[0]):
            await self.game.update(inter)
        else:
            await self.game.stop(inter)


class FramedSelect(disnake.ui.View):
    def __init__(self, game: FramedGame) -> None:
        self.game = game
        super().__init__(timeout=None)
        self.add_item(FramedDropdown(game))


class FramedEmbed(disnake.Embed):
    def __init__(self, game: FramedGame) -> None:
        self.game = game
        super().__init__(title=self.game.locale["COMMAND_GAME_FRAME_REPLY"], color=COLOR)

    def update(self) -> None:
        self.clear_fields()
        self.set_image(url=random.choice(self.game.movie.backdrops))
        self.add_field(self.game.locale["COMMAND_GAME_FRAME_FIELD_SCORE"], self.game.score or 0, inline=True)
        self.add_field(self.game.locale["COMMAND_GAME_FRAME_FIELD_RECORD"], self.game.record or "-", inline=True)
        self.add_field(self.game.locale["COMMAND_GAME_FRAME_FIELD_TOP_SCORER"], self.game.top_scorer or "-", inline=True)

    def stop(self) -> None:
        self.set_image(url=disnake.embeds.EmptyEmbed)
        self.title = self.game.locale["COMMAND_GAME_END"]
        members = sorted(self.game.members.items(), key=lambda x: x[1])
        points = self.game.locale["COMMAND_GAME_POINTS"]
        self.description = "\n".join(
            [
                f"{emoji} {member_score[0]} (**{member_score[1]}** {points})"
                for member_score, emoji in zip(members[:5], "🏆🥈🥉🏅🏅")
            ]
        )


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="game", description=DEFAULT["COMMAND_GAME_DESC"])
    async def game(self, inter: disnake.ApplicationCommandInteraction) -> None:
        pass

    @game.sub_command(name="framed", description=DEFAULT["COMMAND_GAME_FRAME_DESC"])
    async def framed(self, inter: disnake.ApplicationCommandInteraction, hide: Choice.boolean = Option.hide) -> None:
        await FramedGame(inter, ephemeral=hide).start()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Games(bot))
