import asyncio
import logging
from concurrent.futures import TimeoutError
from uuid import uuid4

import websockets

from connection import Connection
from helpers.constants import INVALID_FORMAT


class Server:

    def __init__(self, loop, session_class, players=2, timeout=10):
        self.loop = loop
        self.players = players
        self.session_class = session_class
        self.timeout = timeout
        self.connections = []
        self.sessions = []
        self.lock = asyncio.Lock()

    def serve(self, host, port):
        logging.info(f"Server started on {host}:{port}")
        return websockets.serve(self.handle, host, port)

    async def handle(self, ws, _):
        logging.info(f"Received connection from {ws.remote_address}.")
        connection = Connection(self.loop, ws, meta=self.get_meta())

        is_auth = await self.auth(connection)
        if not is_auth:
            return

        logging.info(f"Success auth: {connection}.")
        session = None

        async with self.lock:
            self.connections.append(connection)
            if self.is_ready():
                session = self.prepare_session(self.connections[:self.players])

        if session:
            await self.start_session(session)
        else:
            await self.keep_connection(connection)

    async def auth(self, connection):
        try:
            await asyncio.wait_for(self._auth(connection), timeout=self.timeout)
        except (ConnectionError, TimeoutError):
            logging.warning(f"Connection {connection.ws.remote_address} fails.")
            return False
        return True

    async def _auth(self, connection):
        async for message in connection.messages:
            payload = message.get("payload")
            if message.get("action") != "auth" or payload.get("nickname") is None:
                await connection.send("auth", False, INVALID_FORMAT)
                continue
            token = payload.get("token")
            connection.id = token if token else str(uuid4())
            connection.nickname = payload.get("nickname")
            await connection.send("auth", connection.id)
            break

    def is_ready(self):
        return len(self.connections) >= self.players

    def prepare_session(self, connections):
        for conn in connections:
            self.connections.remove(conn)
        return self.session_class(self.loop, connections)

    async def start_session(self, session):
        logging.info(f"Created {session}.")
        self.sessions.append(session)
        await session.play()
        self.sessions.remove(session)
        logging.info(f"Closed session {session}.")

    async def keep_connection(self, connection):
        await connection.keep()
        try:
            self.connections.remove(connection)
        except ValueError:
            # already removed
            pass
        logging.info(f"Closed connection {connection.ws.remote_address}.")

    def get_meta(self):
        return {"players": self.players, "game": self.session_class.Meta.game_name}
