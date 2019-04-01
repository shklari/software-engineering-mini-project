from Domain.User import User


class StoreOwner(User):

    appointer = 0
    appointees = []
    managers = []

    def __init__(self, username, password, appointer=0):
        super(StoreOwner, self).__init__(username, password)
        self.appointer = appointer
        self.appointees = []
        self.managers = []

    # @abstractmethod # 2.8 # checks if self is an ancestor of user
    def is_superior(self, user): pass

    # @abstractmethod # 2.8
    def remove_appointee(self, owner): pass

    # @abstractmethod # 2.8
    def remove_manager(self, manager): pass
