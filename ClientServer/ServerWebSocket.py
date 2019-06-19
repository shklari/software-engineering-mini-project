
import asyncio
import json
import threading
from log.Log import Log
from ClientServer.Thread import MyThread
import logging


import websockets
from Service.RealTimeAlert import RealTimeAlert

from Service.serviceImpl import ServiceImpl
logger = logging.getLogger('websocket.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logging.basicConfig()

STATE = {'value': 0}

USERS = set()
users_list = []

service = ServiceImpl()

checkinit = service.init("avabash", "123456",21,'')

# #######################################TEST

#service.sign_up("storeowner1", "111", 32, 'israel')
#service.sign_up("storeowner2", "111", 40, 'israel')
#service.sign_up("storeowner3", "111", 40, 'israel')
#service.sign_up("storeman1", "111", 25, 'israel')
#service.login("storeowner1", "111")
#service.create_store("osem", "storeowner1")
#service.add_new_owner("osem", "storeowner2","storeowner1")
#service.add_new_owner("osem", "storeowner3","storeowner1")
#service.add_new_manager('storeman1','osem',{'Edit':True, 'Add':True,'Remove':True})
#service.add_item_to_inventory({'name': 'bamba', 'price': 2, 'category': 'snacks'}, "osem", 100, "storeowner1")
#service.add_item_to_inventory({'name': 'soup', 'price': 10, 'category': 'snacks'}, "osem", 100, "storeowner1")
#service.add_to_cart('osem','soup',2)
#service.add_to_cart('osem','bamba',2)
#service.get_basket()
#service.get_stores()

#service.add_item_to_inventory({'name': 'bamba', 'price': 2, 'category': 'snacks'}, 'aStore', 100, 'aaa')
#service.add_item_to_inventory({'name': 'soup', 'price': 10, 'category': 'snacks'}, 'aStore', 100, 'aaa')
#service.add_to_cart('aStore', 'bamba', 2, 'aaa')
#service.add_to_cart('aStore', 'soup', 2, 'aaa')


# service.sign_up("storeowner1", "111")
# service.sign_up("storeowner2", "111")
# service.sign_up("storeman1", "111")
# service.login("storeowner1", "111")
# service.create_store("osem")
# service.add_item_to_inventory({'name': "bamba", 'price': 20, 'category': "snakes", 'store_name': "osem"}, "osem", 3)

#service.logout("storeowner1")

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


async def register(websocket,data):
    # for x in USERS:
    #     if not x.open:
    #         USERS.remove(x)

    USERS.add(websocket)
    users_list.append({'ws': websocket, 'username': data['username']})


async def unregister(websocket):
    USERS.remove(websocket)


async def helper(answer, action, websocket):
    if action == 'ping':
        ans = state_event({'action': 'pong', 'return_val': 'pong', 'message': 'pong'})
    elif answer.success:
        ans = state_event({'action': 'success', 'return_val': answer.value, 'message': answer.message})
    else:
        ans = state_event({'action': 'fail', 'return_val': answer.value, 'message': answer.message})
    await websocket.send(ans)


async def datahandler(data, websocket):
    service.web = websocket
    print(data)
    if data['action'] == 'signup':
        ans = service.sign_up(data['username'], data['password'], data['age'], data['country'])
    elif data['action'] == 'login':
        guest_to_users(data['username'], {'ip': websocket.local_address[0], 'port': websocket.local_address[1], 'ws': websocket})
        ans = service.login(data['username'], data['password'])
    elif data['action'] == 'search':
        ans = service.search(data['keyword'])
    elif data['action'] == 'logout':
        ans = service.logout(data['username'])
    elif data['action'] == 'create_store':
        ans = service.create_store(data['name'], data['username'])
    elif data['action'] == 'remove_user':
        ans = service.remove_user(data['user_to_remove'], data['username'])
    elif data['action'] == 'get_cart':
        ans = service.get_cart(data['store_name'], data['username'])
    elif data['action'] == 'add_to_cart':
        ans = service.add_to_cart(data['store_name'], data['item_name'], data['quantity'], data['username'])
    elif data['action'] == 'remove_from_cart':
        ans = service.remove_from_cart(data['store_name'], data['item_name'], data['username'])
    elif data['action'] == 'buy_items':
        ans = service.buy_items(data['items'], data['username'], data['supply_details'], data['collect_details'])
    elif data['action'] == 'add_item_to_inventory':
        ans = service.add_item_to_inventory(data['item'], data['store_name'], data['quantity'], data['username'])
    elif data['action'] == 'remove_item_from_inventory':
        ans = service.remove_item_from_inventory(data['item_name'], data['store_name'], data['username'])
    elif data['action'] == 'decrease_item_quantity':
        ans = service.decrease_item_quantity(data['store_name'], data['item_name'], data['quantity'], data['username'])
    elif data['action'] == 'edit_item_price':
        ans = service.edit_item_price(data['store_name'], data['item_name'], data['new_price'], data['username'])
    elif data['action'] == 'add_new_owner':
        ans = service.add_new_owner(data['store_name'], data['new_owner'], data['username'])
    elif data['action'] == 'add_new_manager':
        ans = service.add_new_manager(data['store_name'], data['new_manager'], data['permissions'], data['username'])
    elif data['action'] == 'remove_owner':
        ans = service.remove_owner(data['store_name'], data['owner_to_remove'], data['username'])
    elif data['action'] == 'remove_manager':
        ans = service.remove_manager(data['store_name'], data['manager_to_remove'], data['username'])
    elif data['action'] == 'edit_product':
        ans = service.edit_product(data['name'], data['store_name'], data['quantity'], data['price'], data['username'])
    elif data['action'] == 'shop_all':
        ans = service.shop_all()
    elif data['action'] == 'get_basket':
        ans = service.get_basket(data['username'])
    elif data['action'] == 'get_basket_size':
        ans = service.get_basket_size(data['username'])
    elif data['action'] == 'get_basket_subtotal':
        ans = service.get_basket_subtotal(data['username'])
    elif data['action'] == 'new_guest':
        ans = service.new_guest(data['username'])
    elif data['action'] == 'get_stores':
        ans = service.get_stores()
    elif data['action'] == 'new_guest':
        ans = service.new_guest(data['username'])
    elif data['action'] == 'add_item_policy':
        # policy = {type, combo, quantity, override}
        ans = service.add_item_policy(data['item_name'], data['store_name'], data['policy'], data['username'])
    elif data['action'] == 'add_store_policy':
        # policy = {type, combo, quantity, override}
        ans = service.add_store_policy(data['store_name'], data['policy'], data['username'])
    elif data['action'] == 'approveNewOwner':
        ans = service.approveNewOwner(data['new_owner_name'], data['username'], data['store_name'])
    elif data['action'] == 'has_alert':
        ans = service.has_alert(data['username'])
    elif data['action'] == 'get_notification':
        ans = service.get_notifications(data['username'])
    elif data['action'] == 'remove_user_notifications':
        ans = service.remove_user_notifications(data['username'])
    else:
        logging.error(
            "unsupported event: {}", data)
        return
    await helper(ans, data['action'], websocket)


async def looper(websocket, path):
    # ws = websocket
    # register(websocket) sends user_event() to websocket

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
                await register(websocket,data)
                await datahandler(data, websocket)
    except Exception as e:
        log.set_info('communication failed', 'errorLog')
        print(e)
#        await websocket.send('communication failed')
    #finally:
        #if websocket.open:
        #    await unregister(websocket)

t = MyThread()
t.set(alert,users_list)
t.start()

#pt = PingThread()
#pt.set(alert)
#pt.start()

asyncio.get_event_loop().run_until_complete(websockets.serve(looper, '0.0.0.0', 6789, close_timeout=-1, ping_interval=20, ping_timeout=10))
asyncio.get_event_loop().run_forever()


