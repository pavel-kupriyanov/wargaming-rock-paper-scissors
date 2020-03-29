import asyncio
import logging
import json

import websockets

from helpers.functions import parse_message


class Connection:

    def __init__(self, loop, ws: websockets.WebSocketServerProtocol, meta=None):
        self.loop = loop
        self.ws = ws
        self.meta = meta
        self.id = None
        self.nickname = None
        self.task = None

    def __str__(self):
        return f"<Connection {self.id} ({self.ws.remote_address})>"

    async def recv(self):
        raw_message = await self.ws.recv()
        return parse_message(raw_message)

    async def send(self, action, payload=True, error=None):
        await self._send({"action": action, "payload": payload, "error": error, "meta": self.meta})

    async def _send(self, message_dict):
        await self.ws.send(json.dumps(message_dict))

    @property
    async def messages(self):
        async for raw_message in self.ws:
            yield parse_message(raw_message)

    async def keep(self):
        if not self.task:
            self.task = asyncio.create_task(self._keep())
            self.ws.connection_lost_waiter.add_done_callback(lambda t: self.task.cancel())
        return await self.task

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
