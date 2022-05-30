# -*- coding: utf-8 -*-
import disnake
from disnake.ext import commands

from pypoca.config import COLOR
from pypoca.database import Server
from pypoca.ext import ALL, DEFAULT, Choice, Option
from pypoca.log import log


class Setting(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError) -> None:
        server = Server.get_by_id(inter.guild.id)
        language = server.language if server else DEFAULT_LANGUAGE
        locale = ALL[language]
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title=locale["ERROR_NO_PERMISSION_NAME"], description=locale["ERROR_NO_PERMISSION_DESC"], color=disnake.Color.red())
            await inter.send(embed=embed, ephemeral=True)
        else:
            log.error(f"{inter}. {error}", extra={"locals": locals(), "ctx": vars(inter)}, exc_info=error)

    @commands.slash_command(name="setting", description=DEFAULT["COMMAND_SETTING_DESC"])
    async def slash_setting(self, inter: disnake.ApplicationCommandInteraction) -> None:
        pass

    @commands.has_permissions(administrator=True)
    @slash_setting.sub_command(name="language", description=DEFAULT["COMMAND_LANGUAGE_DESC"])
    async def slash_language(self, inter: disnake.ApplicationCommandInteraction, language: Choice.language = Option.language) -> None:
        Server.update_or_create(id=inter.guild.id, data={"language": language, "region": language[3:]})
        server = Server.get_by_id(inter.guild.id)
        locale = ALL[server.language] if server else DEFAULT
        description = locale["COMMAND_LANGUAGE_REPLY"]
        embed = disnake.Embed(description=description, color=COLOR)
        await inter.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Setting(bot))
