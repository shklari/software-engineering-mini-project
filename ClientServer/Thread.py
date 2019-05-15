import asyncio
from threading import Thread

import json


class MyThread(Thread):
    alert = ''

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._run())
        loop.close()

    def set(self, al):
        self.alert = al

    async def _run(self):
        while True:
            if not self.alert.tasks.empty():
                task = self.alert.tasks.get()
                await task['ws'].send(json.dumps({'action': 'notify', 'message': task['message']}))


# t = MyThread()
# t.start()
# try:
#     t.join()
# except KeyboardInterrupt: pass