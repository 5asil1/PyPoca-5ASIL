# -*- coding: utf-8 -*-
from datetime import datetime

from pony.orm import Database, Optional, PrimaryKey, Required, db_session

db = Database()


class Server(db.Entity):
    id = PrimaryKey(int, size=64)
    language = Optional(str)
    region = Optional(str)
    frame_record = Optional(int)
    higher_record = Optional(int)
    created_on = Required(datetime, default=datetime.utcnow)
    updated_on = Optional(datetime)

    def before_insert(self) -> None:
        self.created_on = datetime.utcnow()
        self.updated_on = datetime.utcnow()

    def before_update(self) -> None:
        self.updated_on = datetime.utcnow()

    @classmethod
    @db_session
    def get_by_id(cls, id: int) -> db.Entity:
        return cls.get(id=id)

    @classmethod
    @db_session
    def update_by_id(cls, id: int, *, data: dict) -> None:
        cls[id].set(**data)

    @classmethod
    @db_session
    def update_or_create(cls, *, id: int, data: dict) -> None:
        cls.update_by_id(id, data=data) if cls.exists(id=id) else cls(id=id, **data)

    @classmethod
    @db_session
    def get_or_create(cls, *, id: int, data: dict = {}) -> db.Entity:
        return cls.get_by_id(id) or cls(id=id, **data)
