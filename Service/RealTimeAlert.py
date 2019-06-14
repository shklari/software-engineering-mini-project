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

    def notify(self, type, group, message):
        # lst = []
        # if group == 'guest':
        #     lst = self.service.guests
        # elif group == 'user':
        #     lst = self.service.users

        for member in group:
            cur = self.find_user_ws(member)
            if cur:
                self.tasks.put({'ws': cur['ws'], 'message': message, 'type': type})

    def find_user_ws(self, user):
        for x in self.service.users:
            if x['username'] == user:
                return x
        return False

