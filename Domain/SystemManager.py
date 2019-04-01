from Domain.User import Guset


class SystemManager(Guset):

    def __init__(self, username, password):
        super(SystemManager, self).__init__(username, password)