import asyncio
import json

import websockets


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port


async def session(nickname):
    uri = "ws://localhost:8888"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "auth", "payload": {"nickname": nickname}}))
        confirm = json.loads(await websocket.recv())
        print(nickname, confirm)
        response = json.loads(await websocket.recv())
        print(nickname, response)
        await websocket.send(json.dumps({"action": "ready_check", "payload": {}}))
        response = json.loads(await websocket.recv())
        print(nickname, response)
        response = json.loads(await websocket.recv())
        print(nickname, response)
        await websocket.send(json.dumps({"action": "pick", "payload": {"pick": "Rock"}}))
        response = json.loads(await websocket.recv())
        print(nickname, response)
        await websocket.send(json.dumps({"action": "pick", "payload": {"pick": "Paper"}}))
        response = json.loads(await websocket.recv())
        print(nickname, response)
        await websocket.recv()
        await websocket.recv()


async def main():
    tasks = [asyncio.create_task(session(str(i))) for i in range(2)]
    return await asyncio.wait(tasks)


asyncio.get_event_loop().run_until_complete(main())
