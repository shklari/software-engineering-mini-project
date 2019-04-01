from Domain.User import User


class SystemManager(User):

    def __init__(self, username, password):
        super(SystemManager, self).__init__(username, password)