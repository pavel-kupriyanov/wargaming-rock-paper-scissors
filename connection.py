import asyncio
import logging
import json

import websockets

from helpers.constants import INITIALIZED
from helpers.functions import parse_message


class Connection:

    def __init__(self, ws: websockets.WebSocketServerProtocol):
        self.ws = ws
        self.state = INITIALIZED
        self.id = None
        self.task = None

    def __str__(self):
        return f"Connection {self.id} ({self.ws.remote_address}) state: {self.state}"

    async def _send(self, message_dict):
        await self.ws.send(json.dumps(message_dict))

    async def _recv(self):
        raw_message = await self.ws.recv()
        return parse_message(raw_message)

    async def send(self, status, payload="ok", error=None):
        await self._send({"status": status, "message": payload, "error": error})

    @property
    async def messages(self):
        async for raw_message in self.ws:
            yield parse_message(raw_message)

    async def keep(self):
        self.task = asyncio.create_task(self._keep())
        self.ws.connection_lost_waiter.add_done_callback(lambda t: self.task.cancel())
        await self.task

    async def _keep(self):
        while True:
            try:
                await asyncio.sleep(10)
                logging.debug(f"Keep connection with {self.ws.remote_address}")
            except Exception as e:
                logging.error(str(e))
                break

    async def close(self):
        if self.task:
            self.task.cancel()
        await self.ws.close()
