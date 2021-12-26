# -*- coding: utf-8 -*-
import os

from disnake.ext.commands import Bot, when_mentioned_or

from pypoca import Config
from pypoca.entities import Server, init_db


class Servers(dict):
    # TODO: remove this from here

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    def __getitem__(self, server_id: int) -> dict:
        if not hasattr(self, str(server_id)):
            server = Server.fetch(id=server_id)
            data = {
                "language": server.language if server else Config.language,
                "region": server.region if server else Config.region,
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
    # TODO: refactor this
    try:
        guilds_ids = list(map(int, Config.guilds_ids.split(",")))
    except Exception:
        guilds_ids = None
    bot = Bot(command_prefix=when_mentioned_or(Config.prefix), test_guilds=guilds_ids)
    bot.servers = Servers(bot)
    bot.config = Config

    for filename in os.listdir("pypoca/cogs"):
        if filename.startswith("_") or not filename.endswith(".py"):
            continue
        cog = os.path.join("pypoca/cogs", filename)
        bot.load_extension(cog[:-3].replace("/", "."))

    init_db(provider=bot.config.database.provider, credentials=bot.config.database.credentials)
    bot.run(bot.config.token)


if __name__ == "__main__":
    run()
