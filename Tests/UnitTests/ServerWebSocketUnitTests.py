import unittest
import json
import websockets
import asyncio


async def test_signup():
    async with websockets.connect('ws://127.0.0.1:6789') as websocket:
        try:
            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            print(ans)
            unittest.TestCase().assertEqual("success", ans['action'])

            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            print(ans)
            unittest.TestCase().assertEqual("fail", ans['action'])

            name = {"action": "signup", "username": "avabatshushan", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            print(ans)
            unittest.TestCase().assertEqual("success", ans['action'])

        except Exception as e:
            print(e)


asyncio.get_event_loop().run_until_complete(test_signup())









