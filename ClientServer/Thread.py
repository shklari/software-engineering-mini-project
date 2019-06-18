import asyncio
from threading import Thread
import websockets

import json


class MyThread(Thread):
    alert = ''

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._run())
        loop.close()

    def set(self, al,UsersList):
        self.UsersList = UsersList
        self.alert = al

    async def _run(self):
        while True:
            if not self.alert.tasks.empty():
                task = self.alert.tasks.get()
                #if task['type'] == 'notify':
                try:
                    ws = task['ws']
                    for us in self.UsersList:
                        if ws.remote_address[0] == us['ws'].remote_address[0] and us['ws'].open and task['user'] == us['username']:
                            task['ws'] = us;
                            ws = us

                    if us['ws'].open:
                        await ws.send(json.dumps({'action': 'notify', 'message': task['message']}))
                    else:
                        print('Websocket NOT connected. Trying to reconnect.')
                except Exception as e:
                    print(e)
                #elif task['type'] == 'toast':
                #    await task['ws'].send(json.dumps({'action': 'toast', 'message': task['message']}))



# t = MyThread()
# t.start()
# try:
#     t.join()
# except KeyboardInterrupt: pass