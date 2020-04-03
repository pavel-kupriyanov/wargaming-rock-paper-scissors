import asyncio
import logging
from concurrent.futures import TimeoutError, CancelledError
from collections import namedtuple

from websockets.exceptions import ConnectionClosed

Pick = namedtuple("Pick", ("player", "choice"))


class Choice:
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"


class Response:
    NOT_ENOUGH_PLAYERS = "Not enough players"
    ALL_PICKS_IS_NONE = "All picks is null"
    COMPLETED = "Completed"


class Action:
    READY_CHECK = 'ready_check'
    PICK = 'pick'
    GAME_RESULT = 'game_result'
    DISCONNECT = 'disconnect'


OPPONENTS = {
    Choice.ROCK: Choice.SCISSORS,
    Choice.PAPER: Choice.ROCK,
    Choice.SCISSORS: Choice.PAPER
}


class RockPaperScissors:
    class Meta:
        game_name = "Rock Paper Scissors"
        min_players = 2

    def __init__(self, loop, connections, ready_timeout=60, pick_timeout=60, round_timeout=3):
        self.loop = loop
        self.ready_timeout = ready_timeout
        self.pick_timeout = pick_timeout
        self.round_timeout = round_timeout
        self.players = [Player(connection, self) for connection in connections]
        self.task = None

    def __str__(self):
        return f"<Session {id(self)} with {[str(player) for player in self.players]}>"

    async def play(self):
        """
        Entry point of game session
        """
        keep = self.keep_players()
        self.task = asyncio.create_task(self._play())
        try:
            await self.task
        except CancelledError:
            await self._close()
        await keep

    async def _play(self):
        """
        Game logic
        """
        logging.info(f"Created {self}.")
        await self.ready_check()
        winner = None
        current_round = 1
        while not winner:
            logging.info(f"Round {current_round}.")
            picks = await self.get_picks()
            correct_picks = [p for p in picks if p.choice]
            winner = self.get_winner(correct_picks)
            choices = [{"nickname": pick.player.user.nickname, "choice": pick.choice} for pick in picks]
            logging.info(f"Picks: {choices}.")
            await self.send_for_all(Action.GAME_RESULT, {"choices": choices, "winner": winner, "round": current_round})
            if not correct_picks:
                await self.close_game(Response.ALL_PICKS_IS_NONE)
                break
            current_round += 1
            await asyncio.sleep(self.round_timeout)
        else:
            winner.player.user.win += 1
            for player in self.players:
                player.user.games += 1
            await self.close_game(Response.COMPLETED)
        logging.info(f"Closed session {self}.")

    async def _close(self):
        """
        Close all player connections
        """
        await run_tasks([player.close() for player in self.players])

    async def keep_players(self):
        """
        Task will run until all players disconnected
        """
        return await run_tasks([player.keep() for player in self.players])

    async def send_for_all(self, action, payload):
        """
        Send message for all players
        """
        return await run_tasks([player.send(action, payload) for player in self.players])

    async def ready_check(self):
        """
        Wait ready confirm from each player
        """
        return await run_tasks([player.remove_if_not_ready() for player in self.players])

    async def get_picks(self):
        """
        Get pick from eah player
        """
        return await run_tasks([player.get_pick() for player in self.players])

    @staticmethod
    def get_winner(picks):
        """
        Get winner from picks
        Example: ROCK win only if all another choices is SCISSORS
        """
        for pick in picks:
            another_picks = picks[:]
            another_picks.remove(pick)
            if all([p.choice == OPPONENTS[pick.choice] for p in another_picks]):
                return pick
        return None

    async def disconnect(self, player):
        """
        Actions after payer disconnected
        """
        if player in self.players:
            self.players.remove(player)
        await self.send_for_all(Action.DISCONNECT, {"player": player.user.nickname})
        if len(self.players) < self.Meta.min_players:
            await self.close_game(Response.NOT_ENOUGH_PLAYERS)

    async def close_game(self, reason):
        """
        Close session
        """
        logging.info(f"{self} closed. Reason: '{reason}'.")
        await self.send_for_all(Action.DISCONNECT, {"reason": reason})
        self.task.cancel()


class Player:

    def __init__(self, connection, session: RockPaperScissors):
        self.connection = connection
        self.session = session
        self.user = connection.user

    def __str__(self):
        return str(f"<Player {self.user.nickname}>.")

    async def keep(self):
        """
        Keep and correct close player connection
        """
        await self.connection.keep()
        logging.info(f"{self} disconnected from {self.session}.")
        await self.close()

    async def send(self, action, payload):
        """
        Send message to player
        """
        try:
            await self.connection.send(action, payload)
        except ConnectionClosed:
            logging.warning(f"Send failed: {self} connection closed.")
            await self.close()

    async def recv(self, timeout=None):
        """
        Read from connection or close by timeout
        """
        try:
            return await asyncio.wait_for(self.connection.recv(), timeout=timeout)
        except (ConnectionError, TimeoutError) as e:
            logging.warning(f"Failed to read from {self}: {str(e)}.")
        except ConnectionClosed:
            logging.warning(f"Read failed: {self} connection closed.")
            await self.close()
        return None

    async def send_and_recv(self, action, payload, timeout=None):
        """
        Shortcut for send and recv
        """
        await self.send(action, payload)
        return await self.recv(timeout)

    async def remove_if_not_ready(self):
        """
        Confirm what player is ready or close connection
        """
        timeout = self.session.ready_timeout
        res = await self.send_and_recv(Action.READY_CHECK, {"timeout": timeout}, timeout)
        if res and res.get("action") == Action.READY_CHECK:
            await self.send(Action.READY_CHECK, {"status": True})
            return True
        logging.info(f"{self} is not ready. Disconnect.")
        await self.close()
        return False

    async def get_pick(self):
        """
        Get pick from player
        """
        timeout = self.session.pick_timeout
        res = await self.send_and_recv(Action.PICK, {"timeout": timeout}, timeout)

        if res is None:
            logging.info(f"{self} is not pick anything.")
            await self.send(Action.PICK, {"status": False})
            return Pick(self, None)

        action, payload = res.get("action"), res.get("payload")
        if action == "pick" and payload.get("pick") in OPPONENTS.keys():
            await self.send(Action.PICK, {"status": True})
            return Pick(self, payload.get("pick"))
        else:
            await self.send(Action.PICK, {"status": False})
            return Pick(self, None)

    async def close(self):
        await self.session.disconnect(self)
        await self.connection.close()


async def run_tasks(tasks):
    """
    Run tasks and await all
    """
    tasks = [asyncio.create_task(task) for task in tasks]
    return await asyncio.gather(*tasks)
