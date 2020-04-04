import asyncio
import json

from websockets.exceptions import ConnectionClosed

import backend.settings as settings


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
        self.closed = False

    def _write_into(self, message):
        self.input.append(message)

    def _read_from(self):
        return self.output.pop()

    async def recv(self):
        if self.closed:
            raise ConnectionClosed(1000, "bar")
        while True:
            try:
                return self.input.pop()
            except IndexError:
                await asyncio.sleep(1)

    async def send(self, message):
        if self.closed:
            raise ConnectionClosed(1000, "bar")
        self.output.append(message)

    async def close(self):
        self.closed = True
        self.connection_lost_waiter.callback(1)


def write(ws, message):
    ws._write_into(json.dumps(message))


def read(ws):
    return json.loads((ws._read_from()))
