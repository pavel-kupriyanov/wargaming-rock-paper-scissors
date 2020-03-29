import asyncio
import logging

import settings

from server import Server
from games.rock_paper_scissors import RockPaperScissors


def main():
    logging.basicConfig(level=logging.INFO)
    game_server = Server(settings.PLAYERS, RockPaperScissors)
    serve = game_server.serve(settings.HOST, settings.PORT)
    asyncio.get_event_loop().run_until_complete(serve)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
