from Domain.User import User


class SystemManager(User):

    def __init__(self, username, password, age, country):
        super(SystemManager, self).__init__(username, password, age, country)