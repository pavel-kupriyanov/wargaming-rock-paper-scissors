import asyncio
import json
import logging


def parse_message(message: str):
    try:
        res = json.loads(message)
    except json.JSONDecodeError:
        message = f"Invalid message: {message}"
        logging.error(message)
        raise ConnectionError(message)
    return res


async def run_tasks(tasks):
    tasks = [asyncio.create_task(task) for task in tasks]
    return await asyncio.wait(tasks)
