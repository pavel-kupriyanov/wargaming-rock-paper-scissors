import asyncio
import json

import aiounittest

from server import User
from connection import Connection, parse_message

from .utils import MockWebsocket, long_time_test


class TestConnection(aiounittest.AsyncTestCase):

    def setUp(self):
        loop = asyncio.get_event_loop()
        self.ws = MockWebsocket()
        self.connection = Connection(self.ws, loop)

    def test_meta(self):
        self.connection._meta = {"foo": "bar"}
        self.connection.user = User("Vladimir Harkonnen")
        self.assertDictEqual({"foo": "bar", "user": self.connection.user.serialize()}, self.connection.meta)

    async def test_recv(self):
        payload = {"payload": {"foo": "bar"}}
        self.ws._write_into(json.dumps(payload))
        self.assertEqual(payload, await self.connection.recv())

    async def test_send(self):
        payload = {"bar": "baz"}
        await self.connection.send("foo", payload)
        self.assertDictEqual(payload, json.loads(self.ws._read_from())["payload"])

    @long_time_test
    async def test_OK_keep(self):
        task = asyncio.create_task(self.connection.keep())
        await asyncio.sleep(0.2)
        await self.ws.close()
        await asyncio.sleep(0.2)
        self.assertTrue(task.done())

    @long_time_test
    async def test_ERROR_keep(self):
        task = asyncio.create_task(self.connection.keep())
        task.cancel()
        await asyncio.sleep(0.2)
        self.assertTrue(task.cancelled())

    @long_time_test
    async def test_OK_under_keep(self):
        task = asyncio.create_task(self.connection._keep())
        await asyncio.sleep(0.2)
        self.assertFalse(task.done())

    @long_time_test
    async def test_close(self):
        connection = self.connection
        task = asyncio.create_task(connection.keep())
        await asyncio.sleep(0.2)
        connection.user = User("Vladimir Harkonnen")
        connection.user.connected_now = True
        await connection.close()
        await task
        self.assertFalse(connection.user.connected_now)

    def test_OK_parse_message(self):
        message = parse_message('{"action": "test", "payload": {"foo": "bar"}}')
        self.assertIsInstance(message, dict)

    def test_ERROR_format_parse_message(self):
        self.assertRaises(ConnectionError, parse_message, "message")

    def test_ERROR_payload_parse_message(self):
        self.assertRaises(ConnectionError, parse_message, "{'action': 'test'}")
