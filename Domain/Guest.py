from .Basket import Basket


class Guest:
    def __init__(self):
        self.logged_in = False
        self.basket = Basket()

    # @abstractmethod # 2.6
    def add_to_cart(self, store, item, quantity):
        cart = self.basket.get_cart_by_store(store)
        cart.add_item_to_cart(item, quantity)

    # @abstractmethod # 2.7
    def get_cart(self, store):
        return self.basket.get_cart_by_store(store)

    # @abstractmethod # 2.7
    def edit_cart(self, cart, params): pass

    # @abstractmethod # 2.8
    def buy_item(self, item): pass

    def remove_from_cart(self, store, item):
        return self.basket.get_cart(store).remove_item_from_cart(item)
