# Interface
class SystemInterface(object):

    sysManager = 0
    curUser = 0
    users = []
    stores = []

    # @abstractmethod # 1.1
    def init(self, system_manager): pass

    # @abstractmethod # 2.2
    def sign_up(self, username, password): pass

    # @abstractmethod # 2.3
    def login(self, username, password): pass

    # @abstractmethod # 2.4
    def search(self, param): pass

    # @abstractmethod # 2.8
    def buy_items(self, items): pass

    # @abstractmethod # 3.1
    def logout(self): pass

    # @abstractmethod # 3.2
    def create_store(self, name): pass
    # @abstractmethod # 6.2

    def remove_client(self, client): pass

