import asyncio
import logging
from concurrent.futures import TimeoutError
from uuid import uuid4

import websockets

from connection import Connection
from helpers.constants import WAITING, PREPARING, INVALID_FORMAT


class Server:

    def __init__(self, session_class, players=2, timeout=10):
        self.players = players
        self.session_class = session_class
        self.timeout = timeout
        self.connections = []
        self.lock = asyncio.Lock()

    async def handle(self, ws: websockets.WebSocketServerProtocol, _):
        logging.info(f"Received connection from {ws.remote_address}.")
        connection = Connection(ws)

        try:
            await asyncio.wait_for(self.auth(connection), timeout=self.timeout)
        except (ConnectionError, TimeoutError) as e:
            logging.info(f"Connection {ws.remote_address} fails.")
            await ws.close()
            return

        logging.info(f"Success auth: {connection}.")
        session = None

        async with self.lock:
            self.connections.append(connection)
            connection.state = WAITING
            waiting_connections = [conn for conn in self.connections if conn.state == WAITING]
            if len(waiting_connections) >= self.players:
                session = self.get_session(waiting_connections[:self.players])

        if session:
            logging.info(f"Created {session}.")
            await session.play()
        else:
            await connection.keep()
            if connection.state == WAITING:
                self.connections.remove(connection)

        logging.info(f"Closed connection {ws.remote_address}.")

    async def auth(self, connection):
        async for message in connection.messages:
            if message.get("type") == "auth":
                token = message.get("token")
                connection.id = token if token else str(uuid4())
                await connection.send(True, connection.id)
                break
            else:
                await connection.send(False, "Invalid message format.", INVALID_FORMAT)

    def get_session(self, connections):
        for conn in connections:
            self.connections.remove(conn)
            conn.state = PREPARING
        return self.session_class(connections)

    def serve(self, host, port):
        logging.info(f"Server started on {host}:{port}")
        return websockets.serve(self.handle, host, port)
