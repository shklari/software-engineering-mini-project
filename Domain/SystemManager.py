from Domain.Client import Client


class SystemManager(Client):

    def __init__(self, username, password):
        super(SystemManager, self).__init__(username, password)