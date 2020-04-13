import os

HOST = os.getenv('HOST') or 'localhost'
PORT = os.getenv('PORT') or 8888
try:
    PLAYERS = int(os.getenv('PLAYERS')) or 2
except TypeError:
    PLAYERS = 2
try:
    TIMEOUT = int(os.getenv('TIMEOUT')) or 60
except TypeError:
    TIMEOUT = 60
