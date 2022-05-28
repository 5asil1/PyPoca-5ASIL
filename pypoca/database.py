# -*- coding: utf-8 -*-
from datetime import datetime

from pony.orm import Database, Optional, PrimaryKey, Required, db_session

db = Database()


class Server(db.Entity):
    id = PrimaryKey(int, size=64)
    language = Optional(str)
    region = Optional(str)
    created_on = Required(datetime, default=datetime.utcnow)
    updated_on = Optional(datetime)

    def before_insert(self) -> None:
        self.created_on = datetime.utcnow()
        self.updated_on = datetime.utcnow()

    def before_update(self) -> None:
        self.updated_on = datetime.utcnow()

    @staticmethod
    @db_session
    def get_by_id(server_id: int) -> dict:
        if Server.exists(id=server_id):
            return Server[server_id]

    @staticmethod
    @db_session
    def set_by_id(server_id: int, *, data: dict) -> None:
        if Server.exists(id=server_id):
            Server[server_id].set(**data)
        else:
            Server(id=server_id, **data)
