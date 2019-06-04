import queue
from asyncio import Queue


class RealTimeAlert(object):

    def __init__(self, service):
        self.group = []
        self.data = {}
        self.service = service
        self.tasks = queue.Queue(20)

    def add_to_group(self, websocket):
        self.group({})
        websocket.getpeername()

    def notify(self, message, group):
        lst = []
        if group == 'guest':
            lst = self.service.guests
        elif group == 'user':
            lst = self.service.users

        for member in lst:
            self.tasks.put({'ws': member['ws'], 'message': message})

