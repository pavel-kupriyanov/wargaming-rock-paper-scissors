import asyncio
from unittest.mock import Mock

from aiounittest import futurized
from aiounittest.mock import AsyncMockIterator

import settings


class MockSession:
    class Meta:
        game_name = "Mock"

    def __init__(self, loop, connections, **kwargs):
        self.loop = loop
        self.connections = connections
        for k, v in kwargs:
            setattr(self, k, v)

    async def play(self):
        for connection in self.connections:
            await connection.send("game", {"status": True})


class MockWebsocket:
    class ConnectionLostWaiter:

        def __init__(self):
            self.callback = None

        def add_done_callback(self, callback):
            self.callback = callback

    remote_address = '127.0.0.1'

    def __init__(self):
        self.input = []
        self.output = []
        self.connection_lost_waiter = self.ConnectionLostWaiter()

    def _write_into(self, message):
        self.input.append(message)

    def _read_from(self):
        return self.output.pop()

    async def recv(self):
        while True:
            try:
                return self.input.pop()
            except IndexError:
                await asyncio.sleep(1)

    async def send(self, message):
        self.output.append(message)

    async def close(self):
        self.connection_lost_waiter.callback(1)


def long_time_test(func):
    async def wrap(self, *args, **kwargs):
        if settings.RUN_TESTS_WITH_TIMEOUT:
            return await func(self, *args, **kwargs)

    return wrap
