# -*- coding: utf-8 -*-
from discord.ext.commands import Bot
from dislash import InteractionClient

from pypoca.config import Config


def run() -> None:
    """Instantiate, configure and run the bot.

    Connect to Discord client (WebSocket and API). Load all cogs. Start the health
    check server. And finally, run a loop event initialization blocking call.
    """
    bot = Bot(command_prefix=None, help_command=None)
    client = InteractionClient(bot, test_guilds=Config.bot.guilds_ids)

    for cog in Config.bot.cogs:
        cog = cog[:-3].replace("/", ".")
        bot.load_extension(cog)

    bot.run(Config.bot.token)
    client.teardown()


if __name__ == "__main__":
    run()
