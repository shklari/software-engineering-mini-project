from Domain import Client
# Interface


class StoreOwner(Client):

    appointer = 0
    appointees = []
    managers = []

    def _init_(self, new_name, new_password, appointer=0):
        super()._init_(new_name, new_password)
        self.appointer = appointer
        self.appointees = []
        self.managers = []

    # @abstractmethod # 2.8 # checks if self is an ancestor of user
    def is_superior(self, user): pass

    # @abstractmethod # 2.8
    def remove_appointee(self, owner): pass

    # @abstractmethod # 2.8
    def remove_manager(self, manager): pass
