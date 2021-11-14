# -*- coding: utf-8 -*-
from discord.ext.commands import Bot
from dislash import InteractionClient

from pypoca.config import BotConfig


def run() -> None:
    """Instantiate, configure and run the bot.

    Connect to Discord client (WebSocket and API). Load all cogs. Start the health
    check server. And finally, run a loop event initialization blocking call.
    """
    bot = Bot(command_prefix=BotConfig.prefix)
    client = InteractionClient(bot, test_guilds=BotConfig.guilds_ids)

    for cog in BotConfig.cogs:
        cog = cog[:-3].replace("/", ".")
        bot.load_extension(cog)

    bot.run(BotConfig.token)
    client.teardown()


if __name__ == "__main__":
    run()
