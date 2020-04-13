import asyncio
import logging
import json

from concurrent.futures import CancelledError


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
        :return: dict of server metadata
        """
        meta = self._meta
        if self.user:
            meta["user"] = self.user.to_dict()
        return meta

    async def recv(self):
        """
        Read from socket and parse to dict
        :return: dict of user message
        """
        raw_message = await self.ws.recv()
        return parse_message(raw_message)

    async def send(self, action, payload):
        """
        Write to socket
        :param action: type of message
        :param payload: data of message
        :return: None
        """
        message = {"action": action, "payload": payload, "meta": self.meta}
        await self.ws.send(json.dumps(message))

    async def keep(self):
        """
        Keep connection until client close it.
        :return: Task that live until user close connection
        """
        if not self.task:
            self.task = asyncio.create_task(self._keep())
            self.ws.connection_lost_waiter.add_done_callback(lambda t: self.task.cancel())
        return await self.task

    async def _keep(self):
        """
        Endless task that run while True until receive CancelledError (from outside)
        :return: None
        """
        while True:
            try:
                await asyncio.sleep(10)
                logging.debug(f"Keep connection with {self.ws.remote_address}")
            except CancelledError as e:
                logging.debug(f"Keeping error: {str(e)}")
                break

    async def close(self):
        """
        Cancel main connection task to connection correct closing.
        :return: None
        """
        if self.task:
            self.task.cancel()
        self.user.connected_now = False
        await self.ws.close()


def parse_message(message: str):
    """
    Parse json string to dict.
    :param message - raw string
    :return: dict or raise ConnectionError
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
