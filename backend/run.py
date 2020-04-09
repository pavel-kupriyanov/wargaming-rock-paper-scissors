import asyncio
import logging

from .server import Server, settings
from .games.rock_paper_scissors import RockPaperScissors


def main():
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    game_server = Server(loop, RockPaperScissors, players=settings.PLAYERS, timeout=settings.TIMEOUT)
    serve = game_server.serve(settings.HOST, settings.PORT)
    loop.run_until_complete(serve)
    loop.run_forever()


if __name__ == '__main__':
    main()
