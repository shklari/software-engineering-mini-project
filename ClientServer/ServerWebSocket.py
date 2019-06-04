
import asyncio
import json
import logging
import threading
from log.Log import Log
from ClientServer.Thread import MyThread

import websockets
from Service.RealTimeAlert import RealTimeAlert

from Service.serviceImpl import ServiceImpl

logging.basicConfig()

STATE = {'value': 0}

USERS = set()

service = ServiceImpl()

checkinit = service.init("avabash", "123456")

# #######################################TEST
service.sign_up("try2", "111")
service.sign_up("storeowner2", "111")
service.sign_up("storeman1", "111")
service.login("storeowner2", "111")
service.create_store("shaiozim baam")
service.add_new_manager('shaiozim baam','try2',{'Edit':True,'Remove':True,'Add':True})
service.logout()
# service.logout()

# #######################################TEST
ws = 0
alert = service.ownersAlert

log = Log("", "")

print(checkinit.message)


async def run():
    while 1:
        if not alert.tasks.empty():
            task = alert.tasks.get()
            await task['ws'].send(task['message'])


def guest_to_users(username, client):
    for guest in service.guests:
        if guest['ip'] == client['ip']:
            service.users.append({'ip': client['ip'], 'port': client['port'], 'username': username, 'ws': client['ws']})
            service.guests.remove(guest)


def state_event(obj):
    return json.dumps(obj)


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def helper(answer, action, websocket):
    if answer.success:
        ans = state_event({'action': 'success', 'return_val': answer.value, 'message': answer.message})
    else:
        ans = state_event({'action': 'fail', 'return_val': answer.value, 'message': answer.message})
    await websocket.send(ans)


async def datahandler(data, websocket):
    service.web = websocket
    print(data)
    if data['action'] == 'signup':
        ans = service.sign_up(data['username'], data['password'])
    elif data['action'] == 'login':
        guest_to_users(data['username'], {'ip': websocket.local_address[0], 'port': websocket.local_address[1], 'ws': websocket})
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
    ws = websocket
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    # while not websocket.open:
    #   await websockets.connect('ws://100.10.102.7:6789')
    try:
        if websocket.open:
            client = websocket.local_address
            service.guests.append({'ip': client[0], 'port': client[1], 'ws': websocket})
            # alert.notify("hello guest", 'guest')
            async for message in websocket:
                print(message)
                data = json.loads(message)
                print(data)
                await datahandler(data, websocket)
    except Exception as e:
        log.set_info('communication failed', 'errorLog')
        print(e)
        await ws.send('communication failed')
    finally:
        if websocket.open:
            await unregister(websocket)

t = MyThread()
t.set(alert)
t.start()

asyncio.get_event_loop().run_until_complete(websockets.serve(looper, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()


