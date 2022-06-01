# -*- coding: utf-8 -*-
import disnake
from disnake.ext import commands

from pypoca.config import COLOR, URLS
from pypoca.database import Server
from pypoca.ext import ALL, DEFAULT, Choice, Option


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="ping", description=DEFAULT["COMMAND_PING_DESC"])
    async def slash_ping(self, inter: disnake.ApplicationCommandInteraction, hide: Choice.boolean = Option.hide):
        server = Server.get_by_id(inter.guild.id)
        locale = ALL[server.language] if server else DEFAULT
        
        latency = int(self.bot.latency * 1000)
        description = locale["COMMAND_PING_REPLY"] + f": {latency}ms"

        embed = disnake.Embed(description=description, color=COLOR)
        await inter.send(embed=embed, ephemeral=hide)

    @commands.slash_command(name="help", description=DEFAULT["COMMAND_HELP_DESC"])
    async def slash_help(self, inter: disnake.ApplicationCommandInteraction, hide: Choice.boolean = Option.hide):
        server = Server.get_by_id(inter.guild.id)
        locale = ALL[server.language] if server else DEFAULT

        BLANK = "<:blank:914183315056111627>"
        description = f"""
            **/movie**
            {BLANK} **discover** {locale["COMMAND_MOVIE_DISCOVER_DESC"]}
            {BLANK} **find** {locale["COMMAND_MOVIE_FIND_DESC"]}
            {BLANK} **popular** {locale["COMMAND_MOVIE_POPULAR_DESC"]}
            {BLANK} **search** {locale["COMMAND_MOVIE_SEARCH_DESC"]}
            {BLANK} **top** {locale["COMMAND_MOVIE_TOP_DESC"]}
            {BLANK} **trending** {locale["COMMAND_MOVIE_TRENDING_DESC"]}
            {BLANK} **upcoming** {locale["COMMAND_MOVIE_UPCOMING_DESC"]}
            **/tv**
            {BLANK} **discover** {locale["COMMAND_TV_DISCOVER_DESC"]}
            {BLANK} **popular** {locale["COMMAND_TV_POPULAR_DESC"]}
            {BLANK} **search** {locale["COMMAND_TV_SEARCH_DESC"]}
            {BLANK} **top** {locale["COMMAND_TV_TOP_DESC"]}
            {BLANK} **trending** {locale["COMMAND_TV_TRENDING_DESC"]}
            {BLANK} **upcoming** {locale["COMMAND_TV_UPCOMING_DESC"]}
            **/people**
            {BLANK} **popular** {locale["COMMAND_PERSON_POPULAR_DESC"]}
            {BLANK} **search** {locale["COMMAND_PERSON_SEARCH_DESC"]}
            {BLANK} **trending** {locale["COMMAND_PERSON_TRENDING_DESC"]}
            **/game**
            {BLANK} **frame** {locale["COMMAND_GAME_FRAME_DESC"]}
            {BLANK} **higher** {locale["COMMAND_GAME_HIGHER_DESC"]}
            **/setting**
            {BLANK} **language** {locale["COMMAND_LANGUAGE_DESC"]}
        """
        buttons = [
            {"style": 5, "label": locale["COMMAND_HELP_BUTTON_INVITE"], "url": URLS["invite"]},
            {"style": 5, "label": locale["COMMAND_HELP_BUTTON_VOTE"], "url": URLS["vote"]},
            {"style": 5, "label": locale["COMMAND_HELP_BUTTON_SERVER"], "url": URLS["server"]},
            {"style": 5, "label": locale["COMMAND_HELP_BUTTON_SITE"], "url": URLS["site"]},
        ]

        embed = disnake.Embed(description=description, color=COLOR)
        view = disnake.ui.View()
        [view.add_item(disnake.ui.Button(**button)) for button in buttons]
        await inter.send(embed=embed, view=view, ephemeral=hide)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(General(bot))
