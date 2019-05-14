
import asyncio
import json
import logging
import websockets
from Service.RealTimeAlert import RealTimeAlert

from Service.serviceImpl import ServiceImpl

logging.basicConfig()

STATE = {'value': 0}

USERS = set()

service = ServiceImpl()

checkinit = service.init("avabash", "123456")

alert = RealTimeAlert()

print(checkinit.message)


def state_event(obj):
    return json.dumps(obj)


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})


async def register(websocket):
    print("register:")
    print(websocket)
    USERS.add(websocket)


async def unregister(websocket):
    print("unregister:")
    USERS.remove(websocket)


async def helper(answer, action, websocket):
    print("got " + action + " request")
    if answer.success:
        ans = state_event({'action': 'success', 'return_val': answer.value, 'message': answer.message})
    else:
        ans = state_event({'action': 'fail', 'return_val': answer.value, 'message': answer.message})
    print(ans)
    await websocket.send(ans)


async def datahandler(data, websocket):
    service.web = websocket
    if data['action'] == 'signup':
        print(data['username'] + ' ' + data['password'])
        ans = service.sign_up(data['username'], data['password'])
    elif data['action'] == 'login':
        ans = service.login(data['username'], data['password'])
    elif data['action'] == 'search':
        ans = service.search(data['keyword'])
    elif data['action'] == 'logout':
        ans = service.logout()
    elif data['action'] == 'create_store':
        ans = service.create_store(data['name'])
    elif data['action'] == 'remove_user':
        ans = service.remove_user(data['username'])
    elif data['action'] == 'get_cart':
        ans = service.get_cart(data['store_name'])
    elif data['action'] == 'add_to_cart':
        ans = service.add_to_cart(data['store_name'], data['item_name'], data['quantity'])
    elif data['action'] == 'remove_from_cart':
        ans = service.remove_from_cart(data['store_name'], data['item_name'])
    elif data['action'] == 'buy_items':
        ans = service.buy_items(data['items'])
    elif data['action'] == 'add_item_to_inventory':
        ans = service.add_item_to_inventory(data['item'], data['store_name'], data['quantity'])
    elif data['action'] == 'remove_item_from_inventory':
        ans = service.remove_item_from_inventory(data['item_name'], data['store_name'])
    elif data['action'] == 'decrease_item_quantity':
        ans = service.decrease_item_quantity(data['store_name'], data['item_name'], data['quantity'])
    elif data['action'] == 'edit_item_price':
        ans = service.edit_item_price(data['store_name'], data['item_name'], data['new_price'])
    elif data['action'] == 'add_new_owner':
        ans = service.add_new_owner(data['store_name'], data['new_owner'])
    elif data['action'] == 'add_new_manager':
        ans = service.add_new_manager(data['store_name'], data['new_manager'], data['permissions'])
    elif data['action'] == 'remove_owner':
        ans = service.remove_owner(data['store_name'], data['owner_to_remove'])
    elif data['action'] == 'remove_manager':
        ans = service.remove_manager(data['store_name'], data['manager_to_remove'])
    else:
        logging.error(
            "unsupported event: {}", data)
        return
    await helper(ans, data['action'], websocket)


async def looper(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    # while not websocket.open:
    #   await websockets.connect('ws://100.10.102.7:6789')
    try:
        if websocket.open:
            async for message in websocket:
                print(message)
                data = json.loads(message)
                print(data)
                await datahandler(data, websocket)
    except Exception as e:
        print(e)
    finally:
        if websocket.open:
            await unregister(websocket)


asyncio.get_event_loop().run_until_complete(websockets.serve(looper, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()

