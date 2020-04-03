import asyncio
import logging
import json


class Connection:

    def __init__(self, ws, loop, meta=None):
        self.ws = ws
        self.loop = loop
        self._meta = meta or {}
        self.user = None
        self.task = None

    def __str__(self):
        return f"<Connection {self.user.nickname if self.user else ''} ({self.ws.remote_address})>"

    @property
    def meta(self):
        """
        Server meta info
        """
        meta = self._meta
        if self.user:
            meta["user"] = self.user.serialize()
        return meta

    async def recv(self):
        """
        Read from socket
        """
        raw_message = await self.ws.recv()
        return parse_message(raw_message)

    async def send(self, action, payload):
        """
        Write to socket
        """
        message = {"action": action, "payload": payload, "meta": self.meta}
        await self.ws.send(json.dumps(message))

    @property
    async def messages(self):
        """
        Async read from socket
        """
        async for raw_message in self.ws:
            yield parse_message(raw_message)

    async def keep(self):
        """
        Run until socket closed
        """
        if not self.task:
            self.task = asyncio.create_task(self._keep())
            self.ws.connection_lost_waiter.add_done_callback(lambda t: self.task.cancel())
        return await self.task

    async def _keep(self):
        """
        Await until exception
        """
        while True:
            try:
                await asyncio.sleep(10)
                logging.debug(f"Keep connection with {self.ws.remote_address}")
            except Exception as e:
                logging.debug(f"Keeping error: {str(e)}")
                break

    async def close(self):
        """
        Correct close socket
        """
        if self.task:
            self.task.cancel()
        self.user.connected_now = False
        await self.ws.close()


def parse_message(message: str):
    """
    Raw string to message
    """
    try:
        res = json.loads(message)
    except json.JSONDecodeError:
        error_message = f"Invalid message: {message}."
    else:
        payload = res.get('payload')
        if not isinstance(payload, dict):
            error_message = f"Invalid payload {payload}."
        else:
            return res
    logging.error(error_message)
    raise ConnectionError(error_message)
