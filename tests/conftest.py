# -*- coding: utf-8 -*-
import asyncio

import pytest


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
