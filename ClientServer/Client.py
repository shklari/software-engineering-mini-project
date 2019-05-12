import asyncio
#import websockets
import js as js
import websockets
from MarketingSystem.consumers import ChatConsumer

from django.core.serializers import json
import json
import pprint
import websocket



# ws = websockets.WebSocket()
#result = {'action':'signup', 'username': 'ava' , 'password': '123'}
# ws.connect("ws://10.100.102.7", http_proxy_host="localhost", http_proxy_port=6789)
# print("Sending 'Hello, World'...")
# ws.send(json.dump.result)

# async def connect():
#     message = json.dumps({'action':'signup', 'username': 'ava' , 'password': '123'})
#     print("Sending:", message)
#     async with websockets.connect("ws://10.100.102.7:6789") as websocket:
#         await websocket.send(message)
#         response = json.loads(await websocket.recv())
#     print(response)
#
#     ws = ChatConsumer()
#     ws.send()