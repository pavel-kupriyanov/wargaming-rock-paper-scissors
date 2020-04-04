import asyncio
import json

import aiounittest
import websockets

import settings
from server import Server, Error, User
from connection import Connection

from .utils import MockSession, MockWebsocket, long_time_test


class TestServer(aiounittest.AsyncTestCase):
    host = settings.HOST
    port = settings.PORT

    def setUp(self):
        loop = asyncio.get_event_loop()
        self.server = Server(loop, MockSession, players=3)
        self.ws = MockWebsocket()
        self.connection = Connection(self.ws, loop)

    @staticmethod
    def write(ws, message):
        ws._write_into(json.dumps(message))

    @staticmethod
    def read(ws):
        return json.loads((ws._read_from()))

    async def test_meta(self):
        self.assertEqual({"players": 3, "game": MockSession.Meta.game_name}, self.server.meta)

    async def test_serve(self):
        async def echo(websocket, _):
            message = await websocket.recv()
            await websocket.send(message)

        self.server.handle = echo
        serve = self.server.serve(self.host, self.port)
        await asyncio.ensure_future(serve)
        async with websockets.connect(f"ws://{self.host}:{self.port}") as ws:
            await ws.send("foo")
            res = await ws.recv()
        self.assertEqual(res, "foo")

    async def test_OK_under_auth(self):
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        await self.server._auth(self.connection)
        self.assertEqual(True, self.read(self.ws).get("payload").get("status"))

    async def test_ERROR_invalid_format_under_auth(self):
        self.write(self.ws, {"action": "infiltration", "payload": {"nickname": "Vladimir Harkonnen"}})
        await self.server._auth(self.connection)
        self.assertEqual(Error.INVALID_FORMAT, self.read(self.ws).get("payload").get("error"))

    async def test_ERROR_nickname_used_under_auth(self):
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        await self.server._auth(self.connection)
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        await self.server._auth(self.connection)
        self.assertEqual(Error.NICKNAME_USED, self.read(self.ws).get("payload").get("error"))

    async def test_ERROR_already_connected_under_auth(self):
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        await self.server._auth(self.connection)
        token = self.read(self.ws).get("meta").get("user").get("token")
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Leto Atreides", "token": token}})
        await self.server._auth(self.connection)
        self.assertEqual(Error.ALREADY_CONNECTED, self.read(self.ws).get("payload").get("error"))

    async def test_OK_auth(self):
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        res = await self.server.auth(self.connection)
        self.assertEqual(True, res)

    @long_time_test
    async def test_ERROR_timeout_auth(self):
        self.server.timeout = 0.2
        res = await self.server.auth(self.connection)
        self.assertEqual(False, res)

    async def test_prepare_session(self):
        conn1, conn2 = Connection(MockWebsocket(), self.server.loop), Connection(MockWebsocket(), self.server.loop)
        self.server.connections = [conn1, conn2]
        session = self.server.prepare_session([conn1])
        self.assertSequenceEqual([conn1], session.connections)
        self.assertSequenceEqual([conn2], self.server.connections)

    @long_time_test
    async def test_keep_connection(self):
        conn1, conn2 = Connection(MockWebsocket(), self.server.loop), Connection(MockWebsocket(), self.server.loop)
        conn1.user = User("Paul Atreides")
        self.server.connections = [conn1, conn2]
        task = asyncio.create_task(self.server.keep_connection(conn1))
        await asyncio.sleep(0.2)
        self.assertSequenceEqual([conn1, conn2], self.server.connections)
        await conn1.close()
        await task
        self.assertSequenceEqual([conn2], self.server.connections)

    @long_time_test
    async def test_OK_wait_handle(self):
        asyncio.create_task(self.server.handle(self.ws, ""))
        self.write(self.ws, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        await asyncio.sleep(0.2)
        self.assertIs(self.ws, self.server.connections[0].ws)

    @long_time_test
    async def test_OK_create_session_handle(self):
        self.server.players_number = 2

        ws1 = MockWebsocket()
        asyncio.create_task(self.server.handle(ws1, ""))
        self.write(ws1, {"action": "auth", "payload": {"nickname": "Paul Atreides"}})
        ws2 = MockWebsocket()
        asyncio.create_task(self.server.handle(ws2, ""))
        self.write(ws2, {"action": "auth", "payload": {"nickname": "Vladimir Harkonnen"}})
        await asyncio.sleep(0.2)
        res1, res2 = self.read(ws1), self.read(ws2)
        self.assertSequenceEqual([], self.server.connections)
        self.assertEqual("Paul Atreides", res1.get("meta").get("user").get("nickname"))
        self.assertEqual("Vladimir Harkonnen", res2.get("meta").get("user").get("nickname"))

    @long_time_test
    async def test_OK_many_requests_handle(self):
        self.server.players_number = 8
        sockets = []
        for num in range(42):
            ws = MockWebsocket()
            asyncio.create_task(self.server.handle(ws, ""))
            self.write(ws, {"action": "auth", "payload": {"nickname": str(num)}})
            sockets.append(ws)
        await asyncio.sleep(0.2)
        results = []
        for ws in sockets:
            res = self.read(ws)
            if res["action"] == "game":
                results.append(res)
        # two players in queue (42 / 8 = 5 (2))
        self.assertEqual(2, len(self.server.connections))
        # all players with session have a response from MockSession
        self.assertEqual(40, len(results))

    @long_time_test
    async def test_ERROR_not_auth_handle(self):
        self.server.timeout = 1
        asyncio.create_task(self.server.handle(self.ws, ""))
        self.write(self.ws, {"action": "infiltration", "payload": {"nickname": "Vladimir Harkonnen"}})
        await asyncio.sleep(0.2)
        self.assertSequenceEqual([], self.server.connections)

    @long_time_test
    async def test_OK_disconnect_handle(self):
        ws1, ws2 = MockWebsocket(), MockWebsocket()
        asyncio.create_task(self.server.handle(ws1, ""))
        self.write(ws1, {"action": "auth", "payload": {"nickname": "1"}})
        await asyncio.sleep(0.2)
        await ws1.close()
        asyncio.create_task(self.server.handle(ws2, ""))
        self.write(ws2, {"action": "auth", "payload": {"nickname": "2"}})
        await asyncio.sleep(0.2)
        self.assertIs(ws2, self.server.connections[0].ws)


class TestUser(aiounittest.AsyncTestCase):

    async def test_serialize(self):
        user = User("Vladimir Harkonnen")
        self.assertIsInstance(user.serialize(), dict)
