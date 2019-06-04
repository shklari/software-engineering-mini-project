from Domain.User import User


class StoreOwner(User):

    def __init__(self, username, password, age, country, appointer=0):
        super(StoreOwner, self).__init__(username, password, age, country)
        self.appointer = appointer
        self.appointees = []
        self.managers = []

    # @abstractmethod # 2.8 # checks if self is an ancestor of user
    def is_superior(self, user): pass

    # @abstractmethod # 2.8
    def remove_appointee(self, owner): pass

    # @abstractmethod # 2.8
    def remove_manager(self, manager): pass

    def add_appointee(self, user):
        if isinstance(user, User):
            self.appointees.append(user)

    def remove_appointee(self, user):
        if isinstance(user, User):
            self.appointees.remove(user)

    def get_appointees(self):
        return self.appointees

    def is_appointee(self, user):
        if user in self.appointees:
            return True
        return False
