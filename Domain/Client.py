from .User import User


class Client(User):
    def __init__(self, username, password):
        super(Client, self).__init__()
        self.username = username
        self.password = password