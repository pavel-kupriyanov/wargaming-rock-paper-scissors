import asyncio

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


async def run_tasks(tasks):
    """
    Run tasks and await all
    """
    tasks = [asyncio.create_task(task) for task in tasks]
    return await asyncio.gather(*tasks)
