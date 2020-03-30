import asyncio
import logging
from concurrent.futures import TimeoutError
from collections import namedtuple

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

    def __init__(self, loop, connections, ready_timeout=60, pick_timeout=60):
        self.loop = loop
        self.ready_timeout = ready_timeout
        self.pick_timeout = pick_timeout
        self.players = [Player(connection, self) for connection in connections]

    def __str__(self):
        return f"<Session {id(self)} with {[str(p) for p in self.players]}>"

    async def play(self):
        logging.info(f"Created {self}.")
        task = self.keep_connections()
        await self.remove_not_ready_connections()
        winner = None
        while not winner:
            picks = await self.get_picks()

            correct_picks = [p for p in picks if p.choice]
            if not correct_picks:
                await self.close_game(Response.ALL_PICKS_IS_NONE)

            winner = self.get_winner(correct_picks)
            choices = [{"nickname": pick.player.user.nickname, "choice": pick.choice} for pick in picks]

            await self.send_for_all(Action.GAME_RESULT, {"choices": choices, "winner": winner})
            await asyncio.sleep(3)

        winner.player.user.win += 1
        for player in self.players:
            player.user.games += 1
        await self.close_game(Response.COMPLETED)
        await task
        logging.info(f"Closed session {self}.")

    async def keep_connections(self):
        return await run_tasks([p.keep() for p in self.players])

    async def send_for_all(self, action, payload):
        return await run_tasks([p.send(action, payload) for p in self.players])

    async def remove_not_ready_connections(self):
        return await run_tasks([p.remove_if_not_ready() for p in self.players])

    @staticmethod
    def get_winner(picks):
        """
        Example: ROCK win only if all another choices is SCISSORS
        """
        for pick in picks:
            another_choices = [p.choice for p in picks if p is not pick]
            if all([choice == OPPONENTS[pick.choice] for choice in another_choices]):
                return pick
        return None

    async def get_picks(self):
        tasks = run_tasks([p.get_pick() for p in self.players])
        return [res.result() for res in (await tasks)[0]]

    async def disconnect(self, connection):
        if not self.players:
            return
        await self.send_for_all(Action.DISCONNECT, {"player": connection.connection.nickname})
        if len(self.players) < self.Meta.min_players:
            await self.close_game(Response.NOT_ENOUGH_PLAYERS)

    async def close_game(self, reason):
        logging.info(f"{self} closed.")
        await self.send_for_all(Action.DISCONNECT, {"reason": reason})
        return await run_tasks([p.close() for p in self.players])


class Player:

    def __init__(self, connection, session: RockPaperScissors):
        self.connection = connection
        self.session = session
        self.user = connection.user

    def __str__(self):
        return str(f"<Player with {self.connection}>.")

    async def keep(self):
        await self.connection.keep()
        await self.close()
        logging.info(f"{self} disconnected from {self.session}.")
        await self.session.disconnect(self)

    async def send(self, action, payload):
        await self.connection.send(action, payload)

    async def recv(self, timeout=None):
        try:
            message = await asyncio.wait_for(self.connection.recv(), timeout=timeout)
        except (ConnectionError, TimeoutError) as e:
            logging.warning(f"Failed to read from {self}: {str(e)}")
            return None
        return message

    async def remove_if_not_ready(self):
        timeout = self.session.ready_timeout
        await self.send(Action.READY_CHECK, {"timeout": timeout})
        res = await self.recv(timeout)
        if res and res.get("action") == Action.READY_CHECK:
            await self.send(Action.READY_CHECK, {"status": True})
            return True
        logging.info(f"{self} is not ready. Disconnect.")
        await self.close()
        return False

    async def get_pick(self):
        timeout = self.session.pick_timeout
        await self.send(Action.PICK, {"timeout": timeout})
        res = await self.recv(timeout)

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
        if self in self.session.players:
            self.session.players.remove(self)
        await self.connection.close()


async def run_tasks(tasks):
    tasks = [asyncio.create_task(task) for task in tasks]
    return await asyncio.wait(tasks)
