# -*- coding: utf-8 -*-
from discord.ext.commands import Bot
from dislash import InteractionClient

from pypoca.config import BotConfig


if __name__ == "__main__":
    bot = Bot(command_prefix=BotConfig.prefix)
    client = InteractionClient(bot, test_guilds=BotConfig.guilds_ids)

    for cog in BotConfig.cogs:
        cog = cog[:-3].replace("/", ".")
        bot.load_extension(cog)

    bot.run(BotConfig.token)
