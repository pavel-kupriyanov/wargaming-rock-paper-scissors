import asyncio

import aiounittest
from websockets.exceptions import ConnectionClosed

from .utils import MockSession
from ..player import Player
from ..utils import Choice, Pick, Action
from backend.connection import Connection
from backend.server import User
from backend.tests.utils import MockWebsocket, read, write


class PlayerTest(aiounittest.AsyncTestCase):

    def setUp(self):
        loop = asyncio.get_event_loop()
        self.ws = MockWebsocket()
        self.user = User("Vladimir Harkonnen")
        self.connection = Connection(self.ws, loop)
        self.connection.user = self.user
        self.session = MockSession()
        self.player = Player(self.connection, self.session)

    async def test_keep_ok(self):
        task = asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        await self.connection.close()
        await asyncio.sleep(0.1)
        self.assertTrue(task.done())
        self.assertIn(self.player, self.session.removed)

    async def test_send_ok(self):
        payload = {"bar": "baz"}
        await self.player.send("foo", payload)
        await asyncio.sleep(0.1)
        self.assertDictEqual(payload, read(self.ws).get("payload"))

    async def test_send_connection_closed(self):
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        await self.ws.close()
        self.assertRaises(ConnectionClosed, await self.player.send("foo", {"bar": "baz"}))

    async def test_recv_ok(self):
        payload = {"foo": "bar"}
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        write(self.ws, {"action": "test", "payload": payload})
        self.assertDictEqual(payload, (await self.player.recv()).get("payload"))

    async def test_recv_connection_error(self):
        payload = "payload"
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        self.ws._write_into(payload)
        self.assertRaises(ConnectionError, await self.player.recv())

    async def test_recv_connection_closed(self):
        payload = {"foo": "bar"}
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        await self.ws.close()
        self.ws._write_into({"action": "test", "payload": payload})
        self.assertRaises(ConnectionClosed, await self.player.recv())

    async def test_send_and_recv_ok(self):
        payload = {"bar": "baz"}
        write(self.ws, {"action": "test", "payload": payload})
        res = await self.player.send_and_recv("foo", payload)
        await asyncio.sleep(0.1)
        self.assertDictEqual(res.get("payload"), read(self.ws).get("payload"))

    async def test_remove_if_not_ready_ok(self):
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        write(self.ws, {"action": Action.READY_CHECK, "payload":{}})
        res = await self.player.remove_if_not_ready()
        self.assertTrue(res)

    async def test_remove_if_not_ready_timeout(self):
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        res = await self.player.remove_if_not_ready()
        self.assertFalse(res)

    async def test_get_pick_none(self):
        pick = await self.player.get_pick()
        self.assertIsInstance(pick, Pick)
        self.assertEqual(pick.choice, None)

    async def test_get_pick_invalid(self):
        write(self.ws, {"action": "pick", "payload": {"pick": "Lizard"}})
        pick = await self.player.get_pick()
        self.assertIsInstance(pick, Pick)
        self.assertEqual(pick.choice, None)

    async def test_get_pick_ok(self):
        write(self.ws, {"action": "pick", "payload": {"pick": Choice.ROCK}})
        pick = await self.player.get_pick()
        self.assertIsInstance(pick, Pick)
        self.assertEqual(pick.choice, Choice.ROCK)

    async def test_close_ok(self):
        asyncio.create_task(self.player.keep())
        await asyncio.sleep(0.1)
        await self.player.close()
        self.assertIn(self.player, self.session.removed)
