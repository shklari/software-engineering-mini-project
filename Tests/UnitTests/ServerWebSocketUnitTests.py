import unittest
import json
import websockets
import asyncio


async def help_signup():
    async with websockets.connect('ws://127.0.0.1:6789') as websocket:
        try:
            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("fail", ans['action'])

            name = {"action": "signup", "username": "avabatshushan", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

        except Exception as e:
            print(e)

print("test signup start")
asyncio.get_event_loop().run_until_complete(help_signup())
print("test signup end")


async def help_login():
    async with websockets.connect('ws://127.0.0.1:6789') as websocket:
        try:
            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "login", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("fail", ans['action'])
        except Exception as e:
            print(e)

print("test login start")
asyncio.get_event_loop().run_until_complete(help_login())
print("test login end")


async def help_logout():
    async with websockets.connect('ws://127.0.0.1:6789') as websocket:
        try:
            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "login", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "logout"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("fail", ans['action'])
        except Exception as e:
            print(e)


print("test logout start")
asyncio.get_event_loop().run_until_complete(help_logout())
print("test logout end")


async def help_remove_user():
    async with websockets.connect('ws://127.0.0.1:6789') as websocket:
        try:
            name = {"action": "signup", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "login", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

            name = {"action": "logout"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "login", "username": "avabash", "password": "123456"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "remove_user", "user": "ava"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("success", ans['action'])

            name = {"action": "logout"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

            name = {"action": "login", "username": "ava", "password": "123456"}
            await websocket.send(json.dumps(name))
            greeting = await websocket.recv()
            ans = json.loads(greeting)
            unittest.TestCase().assertEqual("fail", ans['action'])

            name = {"action": "logout"}
            await websocket.send(json.dumps(name))
            await websocket.recv()

        except Exception as e:
            print(e)


print("test remove start")
asyncio.get_event_loop().run_until_complete(help_logout())
print("test remove end")
