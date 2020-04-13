import asyncio
import logging
from concurrent.futures import CancelledError

from .player import Player
from .utils import Action, Response, OPPONENTS, run_tasks


class RockPaperScissors:
    class Meta:
        game_name = "Rock Paper Scissors"
        min_players = 2

    def __init__(self, loop, connections, ready_timeout=60, pick_timeout=60, round_timeout=10):
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
        Entry point of game. Game will works until all players disconnect.
        :return: None
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
        Game cycle. Players confirm ready status and choose you picks until one wins.
        :return: None
        """
        logging.info(f"Created {self}.")
        players = [{"nickname": player.user.nickname} for player in self.players]
        await self.send_for_all(Action.GAME_START, {"players": players})
        await self.ready_check()
        winner = None
        current_round = 1
        while not winner:
            logging.info(f"Round {current_round}.")
            picks = await self.get_picks(current_round)
            correct_picks = [p for p in picks if p.choice]
            if not correct_picks:
                await self.close_game(Response.ALL_PICKS_IS_NONE)
                break
            winner = self.get_winner(correct_picks)
            choices = [{"nickname": pick.player.user.nickname, "choice": pick.choice} for pick in picks]
            logging.info(f"Picks: {choices}.")
            message = {"choices": choices, "winner": None, "round": current_round}
            if winner:
                message["winner"] = winner.player.user.nickname
            else:
                current_round += 1
            await self.send_for_all(Action.GAME_RESULT, message)
            await asyncio.sleep(self.round_timeout)
        else:
            winner.player.user.win += 1
            for player in self.players:
                player.user.games += 1
            await self.close_game(Response.COMPLETED)
        logging.info(f"Closed session {self}.")

    async def _close(self):
        """
        Call method close() for each user to close all connections.
        :return: Task that await all players close() method.
        """
        await run_tasks([player.close() for player in self.players])

    async def keep_players(self):
        """
        Create task that will run until all players disconnected.
        :return: Task that live until players connected.
        """
        return await run_tasks([player.keep() for player in self.players])

    async def send_for_all(self, action, payload):
        """
        Send message to all players.
        :param action: Type of message.
        :param payload: Data of message.
        :return: Task that live until all messages sends.
        """
        return await run_tasks([player.send(action, payload) for player in self.players])

    async def ready_check(self):
        """
        Run remove_if_not_ready method fo each player.
        :return: Task that live until all players send "ready" or disconnect.
        """
        return await run_tasks([player.remove_if_not_ready() for player in self.players])

    async def get_picks(self, current_round):
        """
        Waiting picks for each player.
        :param current_round: Number of current game round
        :return: Task that live until all players sends your picks.
        """
        return await run_tasks([player.get_pick(current_round) for player in self.players])

    @staticmethod
    def get_winner(picks):
        """
        Chose winner from picks
        Example: ROCK win only if all another choices is SCISSORS
        :param picks: List of picks from users
        :return: winner pick or None if draw
        """
        for pick in picks:
            another_picks = picks[:]
            another_picks.remove(pick)
            if all([p.choice == OPPONENTS[pick.choice] for p in another_picks]):
                return pick
        return None

    async def disconnect(self, player):
        """
        Actions after payer disconnected - remove player from self.players, send message for other players,
        close game if players count not enough.
        :param player: Player that will be removed.
        :return: None.
        """
        if player in self.players:
            self.players.remove(player)
        await self.send_for_all(Action.DISCONNECT, {"player": player.user.nickname})
        if len(self.players) < self.Meta.min_players:
            await self.close_game(Response.NOT_ENOUGH_PLAYERS)

    async def close_game(self, reason):
        """
        Close game - send message for players, cancel main task to break play() method.
        :param reason: String for end user.
        :return: None
        """
        logging.info(f"{self} closed. Reason: '{reason}'.")
        await self.send_for_all(Action.DISCONNECT, {"reason": reason})
        self.task.cancel()
