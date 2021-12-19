# -*- coding: utf-8 -*-
import os

from discord.ext import commands
from dislash import InteractionClient

from pypoca.config import Config
from pypoca.entities import Server, init_db


class Servers(dict):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    def __getitem__(self, server_id: int) -> dict:
        if not hasattr(self, str(server_id)):
            server = Server.fetch(id=server_id)
            data = {
                "language": server.language if server else Config.bot.language,
                "region": server.region if server else Config.bot.region,
            }
            setattr(self, str(server_id), data)
        return getattr(self, str(server_id))

    def __setitem__(self, server_id: int, data: dict) -> dict:
        Server.update_or_create(id=server_id, **data)
        setattr(self, str(server_id), data)
        return getattr(self, str(server_id))


def run() -> None:
    """Instantiate, configure and run the bot and the database.

    Connect to Discord client (WebSocket and API). Load all cogs. Start the health
    check server. And finally, run a loop event initialization blocking call.
    """
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(Config.bot.prefix))
    try:
        guilds_ids = list(map(int, Config.bot.guilds_ids.split(",")))
    except Exception:
        guilds_ids = None
    client = InteractionClient(bot, test_guilds=guilds_ids)
    bot.servers = Servers(bot)

    for filename in os.listdir("pypoca/cogs"):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue
        cog = os.path.join("pypoca/cogs", filename)
        bot.load_extension(cog[:-3].replace("/", "."))

    init_db(provider=Config.database.provider, credentials=Config.database.credentials)
    bot.run(Config.bot.token)
    client.teardown()


if __name__ == "__main__":
    run()
