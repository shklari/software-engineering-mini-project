# Interface
class User(object):

    basket = 0

    def _init_(self): pass

    # @abstractmethod # 2.6
    def add_to_cart(self, store, items): pass

    # @abstractmethod # 2.7
    def get_cart(self, store): pass

    # @abstractmethod # 2.7
    def edit_cart(self, cart, params): pass

    # @abstractmethod # 2.8
    def buy_item(self, item): pass