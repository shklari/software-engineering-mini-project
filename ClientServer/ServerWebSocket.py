
import asyncio
import json
import logging
import websockets

from Service.serviceImpl import ServiceImpl

logging.basicConfig()

STATE = {'value': 0}

USERS = set()

service = ServiceImpl()

service.init("avabash", "123456")


def state_event(obj):
    return json.dumps(obj)


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})


async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def datahandler(data, websocket):
    if data['action'] == 'signup':
        ans = service.sign_up(data['username'], data['password'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'login':
        ans = service.login(data['username'], data['password'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'search':
        ans = service.search(data['keyword'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'logout':
        ans = service.logout()
        await websocket.send(state_event(ans))
    elif data['action'] == 'create_store':
        ans = service.create_store(data['name'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'remove_user':
        ans = service.remove_user(data['username'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'get_cart':
        ans = service.get_cart(data['store_name'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'add_to_cart':
        ans = service.add_to_cart(data['store_name'], data['item_name'], data['quantity'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'remove_from_cart':
        ans = service.remove_from_cart(data['store_name'], data['item_name'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'buy_items':
        ans = service.buy_items(data['items'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'add_item_to_inventory':
        ans = service.add_item_to_inventory(data['item'], data['store_name'], data['quantity'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'remove_item_from_inventory':
        ans = service.remove_item_from_inventory(data['item_name'], data['store_name'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'decrease_item_quantity':
        ans = service.decrease_item_quantity(data['store_name'], data['item_name'], data['quantity'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'edit_item_price':
        ans = service.edit_item_price(data['store_name'], data['item_name'], data['new_price'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'add_new_owner':
        ans = service.add_new_owner(data['store_name'], data['new_owner'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'add_new_manager':
        ans = service.add_new_manager(data['store_name'], data['new_manager'], data['permissions'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'remove_owner':
        ans = service.remove_owner(data['store_name'], data['owner_to_remove'])
        await websocket.send(state_event(ans))
    elif data['action'] == 'remove_manager':
        ans = service.remove_manager(data['store_name'], data['manager_to_remove'])
        await websocket.send(state_event(ans))
    else:
        logging.error(
            "unsupported event: {}", data)


async def looper(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            datahandler(data, websocket)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(websockets.serve(looper, 'localhost', 6789))
asyncio.get_event_loop().run_forever()
