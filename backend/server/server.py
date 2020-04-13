import asyncio
import logging
from concurrent.futures import TimeoutError
from uuid import uuid4

import websockets

from .connection import Connection


class Error:
    INVALID_FORMAT = {"code": 400, "message": "Invalid format"}
    NICKNAME_USED = {"code": 401, "message": "Nickname already used"}
    ALREADY_CONNECTED = {"code": 403, "message": "User already connected now"}


ACTION_AUTH = "auth"


class Server:

    def __init__(self, loop, session_class, players=2, timeout=10):
        self.loop = loop
        self.players_number = players
        self.session_class = session_class
        self.timeout = timeout
        self.connections = []
        self.users = dict()
        self.lock = asyncio.Lock()

    @property
    def meta(self):
        """
        Server info
        """
        return {"players": self.players_number, "game": self.session_class.Meta.game_name}

    def serve(self, host, port):
        """
        Run web server
        """
        logging.info(f"Server started on {host}:{port}")
        return websockets.serve(self.handle, host, port)

    async def handle(self, ws, _):
        """
        Handle websocket connection
        """
        logging.info(f"Received connection from {ws.remote_address}.")
        connection = Connection(ws, self.loop, meta=self.meta)

        if not await self.auth(connection):
            return

        logging.info(f"Success auth: {connection}.")
        session = None

        async with self.lock:
            self.connections.append(connection)
            if len(self.connections) == self.players_number:
                session = self.prepare_session(self.connections[:self.players_number])

        if session:
            await session.play()
        else:
            await self.keep_connection(connection)
        connection.user.connected_now = False

    async def auth(self, connection):
        """
        Try to auth user until timeout
        """
        try:
            return await asyncio.wait_for(self._auth(connection), timeout=self.timeout)
        except (ConnectionError, TimeoutError):
            logging.warning(f"Connection {connection.ws.remote_address} failed.")
            return False

    async def _auth(self, connection):
        """
        Auth logic
        """
        message = await connection.recv()
        action, payload = message.get("action"), message.get("payload")

        if action != ACTION_AUTH or not isinstance(payload, dict):
            await connection.send(ACTION_AUTH, {"status": False, "error": Error.INVALID_FORMAT})
            return False

        token, nickname = payload.get("token"), payload.get("nickname")
        if nickname in {user.nickname for user in self.users.values() if user.connected_now}:
            await connection.send(ACTION_AUTH, {"status": False, "error": Error.NICKNAME_USED})
            return False

        user = self.users.get(token) or User(nickname)
        if user.connected_now:
            await connection.send(ACTION_AUTH, {"status": False, "error": Error.ALREADY_CONNECTED})
            return False

        user.nickname = nickname
        self.users[user.token] = user
        user.connected_now = True
        connection.user = user
        await connection.send(ACTION_AUTH, {"status": True})
        return True

    def prepare_session(self, connections):
        """
        Remove connections from queue and pass them to game session
        """
        for conn in connections:
            self.connections.remove(conn)
        return self.session_class(self.loop, connections)

    async def keep_connection(self, connection):
        """
        Await until connection closed
        """
        await connection.keep()
        if connection in self.connections:
            self.connections.remove(connection)
        logging.info(f"Closed connection {connection.ws.remote_address}.")


class User:

    def __init__(self, nickname):
        self.nickname = nickname
        self.token = str(uuid4())
        self.connected_now = False
        self.win = 0
        self.games = 0

    def to_dict(self):
        """
        User info to dict
        """
        return {"token": self.token, "nickname": self.nickname, "win": self.win, "games": self.games}
