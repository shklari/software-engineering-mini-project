
class RealTimeAlert(object):

    def __init__(self):
        self.group = []
        self.data = {}

    def add_to_group(self, websocket):
        self.group({})
        websocket.getpeername()

    def notify(self, message):
        for x in self.group:
            await x.send(message)

