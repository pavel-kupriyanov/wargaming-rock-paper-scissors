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
