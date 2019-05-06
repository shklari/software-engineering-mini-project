import unittest
import json
import websocket
import asyncio


# class ServerWebSocketUnitTests(unittest.TestCase):

async def hello():
    ws = websocket.WebSocket("wss:\\100.10.102.7:6789")
    name = {"action": "signup", "username": "ava", "password": "123456"}
    await ws.send(json.dumps(name))
    print(name)

    greeting = await ws.receive()
    print(greeting)
    # self.assertEqual("success", greeting['action'])

    name = {"action": "signup", "username": "ava", "password": "123456"}

    await ws.send(json.dumps(name))
    print(name)

    greeting = await ws.receive()
    print(greeting)
    # self.assertEqual("fail", greeting['action'])


asyncio.get_event_loop().run_until_complete(hello())
# asyncio.get_event_loop().run_until_complete(websockets.serve(hello, '10.100.102.7', 6789))











