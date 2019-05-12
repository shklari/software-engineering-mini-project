
class RealTimeAlert(object):

    def __init__(self):
        self.group = []
        self.data = {}

    def add_to_group(self, user):
        self.group.append(user)

    def notify(self, message): pass
