# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime

from pony.orm import Database, Optional, PrimaryKey, Required, db_session

db = Database()


class Server(db.Entity):
    id = PrimaryKey(int, size=64)
    language = Optional(str)
    region = Optional(str)
    created_on = Required(datetime)
    updated_on = Required(datetime)

    @staticmethod
    @db_session
    def create(id: int, **kwargs) -> Server:
        return Server(id=id, created_on=datetime.utcnow(), updated_on=datetime.utcnow(), **kwargs)

    @staticmethod
    @db_session
    def fetch(id: int) -> Server:
        return Server.get(id=id)

    @staticmethod
    @db_session
    def update(id: int, **kwargs) -> None:
        entity = Server.get_for_update(id=id)
        kwargs["updated_on"] = datetime.utcnow()
        for attr, value in kwargs.items():
            setattr(entity, attr, value)

    @staticmethod
    @db_session
    def fetch_or_create(id: int, **kwargs) -> db.Entity:
        return Server.fetch(id=id, **kwargs) if Server.exists(id=id) else Server.create(id=id, **kwargs)

    @staticmethod
    @db_session
    def update_or_create(id: int, **kwargs) -> None:
        Server.update(id=id, **kwargs) if Server.exists(id=id) else Server.create(id=id, **kwargs)


def init_db(provider: str, credentials: dict) -> Database:
    if provider == "sqlite":
        db.bind(provider=provider, filename=credentials["filename"])
    elif provider == "postgres":
        db.bind(
            provider=provider,
            user=credentials["user"],
            password=credentials["password"],
            host=credentials["host"],
            database=credentials["database"],
        )
    else:
        raise ValueError(f"Databse 'provider' must be 'sqlite' or 'postgres', not {provider}")
    db.generate_mapping(create_tables=True)
