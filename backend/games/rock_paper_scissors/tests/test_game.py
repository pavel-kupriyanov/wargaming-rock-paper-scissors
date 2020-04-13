import asyncio

import aiounittest

from backend.server import User, Connection
from backend.server.tests.utils import MockWebsocket, read, write
from backend.games.rock_paper_scissors import RockPaperScissors, Action, Choice, Pick, Response


class TestGame(aiounittest.AsyncTestCase):

    def setUp(self):
        loop = asyncio.get_event_loop()
        connections = []
        self.sockets = {}
        for nickname in ("Vladimir Harkonnen", "Paul Atreides", "Shaddam Corrino IV"):
            ws = MockWebsocket()
            self.sockets[nickname] = ws
            connection = Connection(ws, loop)
            connection.user = User(nickname)
            connections.append(connection)
        self.game = RockPaperScissors(loop, connections)

    async def test_keep_players_ok(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        self.assertEqual(3, len(self.game.players))
        self.game.task.cancel()
        await asyncio.sleep(0.1)
        self.assertEqual(0, len(self.game.players))

    async def test_send_for_all_ok(self):
        payload = {"foo": "bar"}
        asyncio.create_task(self.game.send_for_all("test", payload))
        await asyncio.sleep(0.1)
        for ws in self.sockets.values():
            self.assertDictEqual(payload, read(ws).get("payload"))

    async def test_ready_check_ok(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        self.game.ready_timeout = 0.1
        asyncio.create_task(self.game.ready_check())
        ws_list = list(self.sockets.values())
        for ws in ws_list[1:]:
            write(ws, {"action": Action.READY_CHECK, "payload": {"status": True}})
        write(ws_list[0], {"action": "Not Ready", "payload": {}})
        await asyncio.sleep(0.2)
        # one player disconnected by timeout
        self.assertEqual(2, len(self.game.players))

    async def test_get_pick_ok(self):
        ws_list = list(self.sockets.values())
        values = (Choice.ROCK, Choice.PAPER, "Lizard")
        for ws, value in zip(ws_list, values):
            write(ws, {"action": "pick", "payload": {"pick": value}})
        choices = [pick.choice for pick in await self.game.get_picks(1)]
        self.assertEqual([Choice.ROCK, Choice.PAPER, None], choices)

    def test_get_winner_ok(self):
        players = self.game.players
        picks = [Pick(players[0], Choice.ROCK), Pick(players[1], Choice.PAPER)]
        winner = self.game.get_winner(picks)
        self.assertEqual(picks[1], winner)

    def test_get_winner_many_players(self):
        players = self.game.players
        picks = [Pick(players[0], Choice.ROCK), Pick(players[1], Choice.PAPER), Pick(players[2], Choice.ROCK)]
        winner = self.game.get_winner(picks)
        self.assertEqual(picks[1], winner)

    def test_get_winner_tie(self):
        players = self.game.players
        picks = [Pick(players[0], Choice.ROCK), Pick(players[1], Choice.PAPER), Pick(players[2], Choice.SCISSORS)]
        winner = self.game.get_winner(picks)
        self.assertIsNone(winner)

    async def test_disconnect_continue(self):
        disconnect_user = self.game.players[0]
        remaining_user = self.game.players[1]
        await self.game.disconnect(disconnect_user)
        message = read(self.sockets[remaining_user.user.nickname])
        self.assertEqual(Action.DISCONNECT, message.get("action"))
        self.assertNotIn(disconnect_user, self.game.players)

    async def test_disconnect_break(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        disconnect1, disconnect2 = self.game.players[0:2]
        remaining_user = self.game.players[2]
        await self.game.disconnect(disconnect1)
        message = read(self.sockets[remaining_user.user.nickname])
        self.assertEqual(Action.DISCONNECT, message.get("action"))
        await self.game.disconnect(disconnect2)
        message = read(self.sockets[remaining_user.user.nickname])
        self.assertEqual(Action.DISCONNECT, message.get("action"))
        message = read(self.sockets[remaining_user.user.nickname])
        self.assertEqual(Action.DISCONNECT, message.get("action"))
        self.assertEqual(Response.NOT_ENOUGH_PLAYERS, message.get("payload").get("reason"))

    async def test_under_close_ok(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        await self.game._close()
        self.assertEqual([], self.game.players)

    async def test_close_game_ok(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        await self.game.close_game(Response.COMPLETED)
        await asyncio.sleep(0.1)
        self.assertEqual([], self.game.players)

    async def test_under_play_ok(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        asyncio.create_task(self.game._play())
        ws_list = list(self.sockets.values())
        winner = ws_list[0]
        for ws in ws_list[1:]:
            write(ws, {"action": Action.READY_CHECK, "payload": {}})
            write(ws, {"action": "pick", "payload": {"pick": Choice.ROCK}})
        write(winner, {"action": Action.READY_CHECK, "payload": {}})
        write(winner, {"action": "pick", "payload": {"pick": Choice.PAPER}})

        await asyncio.sleep(0.1)
        for _ in range(5):
            read(winner)
        message = read(winner)
        self.assertEqual(message.get("payload").get("winner"), "Vladimir Harkonnen")

    async def test_under_play_not_ready(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        self.game.ready_timeout = 0.1
        asyncio.create_task(self.game._play())
        await asyncio.sleep(0.2)
        self.assertEqual([], self.game.players)

    async def test_under_play_not_picks(self):
        self.game.task = asyncio.create_task(self.game.keep_players())
        await asyncio.sleep(0.1)
        self.game.pick_timeout = 0.1
        asyncio.create_task(self.game._play())
        ws_list = list(self.sockets.values())
        for ws in ws_list:
            write(ws, {"action": Action.READY_CHECK, "payload": {}})
        await asyncio.sleep(0.2)
        for _ in range(5):
            read(ws_list[0])
        message = read(ws_list[0])
        self.assertEqual(Response.ALL_PICKS_IS_NONE, message.get("payload").get("reason"))
