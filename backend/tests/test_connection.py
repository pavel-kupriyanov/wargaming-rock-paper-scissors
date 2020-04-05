import asyncio
import json

import aiounittest

from .utils import MockWebsocket
from backend import User, Connection, parse_message


class TestConnection(aiounittest.AsyncTestCase):

    def setUp(self):
        loop = asyncio.get_event_loop()
        self.ws = MockWebsocket()
        self.connection = Connection(self.ws, loop)

    def test_meta_ok(self):
        self.connection._meta = {"foo": "bar"}
        self.connection.user = User("Vladimir Harkonnen")
        self.assertDictEqual({"foo": "bar", "user": self.connection.user.to_dict()}, self.connection.meta)

    async def test_recv_ok(self):
        payload = {"payload": {"foo": "bar"}}
        self.ws._write_into(json.dumps(payload))
        self.assertEqual(payload, await self.connection.recv())

    async def test_send_ok(self):
        payload = {"bar": "baz"}
        await self.connection.send("foo", payload)
        self.assertDictEqual(payload, json.loads(self.ws._read_from())["payload"])

    async def test_keep_ok(self):
        task = asyncio.create_task(self.connection.keep())
        await asyncio.sleep(0.1)
        await self.ws.close()
        await asyncio.sleep(0.1)
        self.assertTrue(task.done())

    async def test_keep_cancel(self):
        task = asyncio.create_task(self.connection.keep())
        task.cancel()
        await asyncio.sleep(0.1)
        self.assertTrue(task.cancelled())

    async def test_under_keep_ok(self):
        task = asyncio.create_task(self.connection._keep())
        await asyncio.sleep(0.1)
        self.assertFalse(task.done())

    async def test_close_ok(self):
        connection = self.connection
        task = asyncio.create_task(connection.keep())
        await asyncio.sleep(0.1)
        connection.user = User("Vladimir Harkonnen")
        connection.user.connected_now = True
        await connection.close()
        await task
        self.assertFalse(connection.user.connected_now)

    def test_parse_message_ok(self):
        message = parse_message('{"action": "test", "payload": {"foo": "bar"}}')
        self.assertIsInstance(message, dict)

    def test_format_parse_message_invalid(self):
        self.assertRaises(ConnectionError, parse_message, "message")

    def test_parse_message_without_payload(self):
        self.assertRaises(ConnectionError, parse_message, "{'action': 'test'}")
