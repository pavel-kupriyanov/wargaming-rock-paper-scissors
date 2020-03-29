import asyncio
import logging
from concurrent.futures import TimeoutError

from connection import Connection

from helpers.constants import NOT_ENOUGH_PLAYERS
from helpers.functions import run_tasks


# TODO: observer
class RockPaperScissors:
    class Meta:
        game_name = 'Rock Paper Scissors'
        min_players = 2
        max_players = 12

    def __init__(self, loop, connections, ready_timeout=60, pick_timeout=10):
        self.loop = loop
        self.connections = [ConnectionWrapper(connection, self) for connection in connections]
        self.ready_timeout = ready_timeout
        self.pick_timeout = pick_timeout

    def __str__(self):
        return f"<Session {id(self)} with {[str(c) for c in self.connections]}>"

    async def play(self):
        task = self.keep_connections()
        await self.remove_not_ready_connections()
        picks = [res.result for res in await self.get_picks()]
        print(picks)
        await task

    async def keep_connections(self):
        return await run_tasks([c.keep() for c in self.connections])

    async def send_for_all(self, message):
        return await run_tasks([c.send(message) for c in self.connections])

    async def remove_not_ready_connections(self):
        return await run_tasks([c.remove_if_not_ready() for c in self.connections])

    async def get_picks(self):
        return await run_tasks([c.get_pick() for c in self.connections])

    async def disconnect(self, connection):
        if not self.connections:
            return
        await self.send_for_all({"action": "disconnect", "payload": {"player": connection.connection.nickname}})
        if len(self.connections) < self.Meta.min_players:
            await self.close_game(NOT_ENOUGH_PLAYERS)

    async def close_game(self, reason):
        logging.info(f"{self} closed.")
        await self.send_for_all({"action": "disconnect_all", "payload": {"reason": reason}})
        return await run_tasks([c.close() for c in self.connections])


class ConnectionWrapper:

    def __init__(self, connection, session: RockPaperScissors):
        self.connection = connection
        self.session = session

    def __str__(self):
        return self.connection.__str__()

    async def keep(self):
        await self.connection.keep()
        await self.close()
        logging.info(f"{self} disconnected disconnected from {self.session}.")
        await self.session.disconnect(self)

    async def send(self, message):
        await self.connection.send(**message)

    async def receive(self, timeout=None):
        try:
            message = await asyncio.wait_for(self.connection.recv(), timeout=timeout)
        except (ConnectionError, TimeoutError) as e:
            logging.warning(f"Failed to read from {self}.")
            return None
        return message

    async def remove_if_not_ready(self):
        timeout = self.session.ready_timeout
        message = {"action": "ready_check", "payload": {"timeout": timeout}}
        await self.send(message)
        res = await self.receive(timeout)
        if res is None:
            logging.info(f"{self} is not ready. Disconnect.")
            await self.close()
        elif res.get("action") == "ready_check" and res.get("payload"):
            await self.send({"action": "ready", "payload": True})
            return True
        return False

    async def get_pick(self):
        timeout = self.session.pick_timeout
        message = {"action": "pick", "payload": {"timeout": timeout}}
        await self.send(message)
        res = await self.receive(timeout)
        if res is None:
            logging.info(f"{self} is not pick anything.")
            await self.send({"action": "pick", "payload": False})
        elif res.get("action") == "pick" and res.get("payload"):
            await self.send({"action": "pick", "payload": True})
            return self.connection.id, res.get("payload")
        return self.connection.id, None

    async def close(self):
        try:
            self.session.connections.remove(self)
        except ValueError:
            pass
        await self.connection.close()
