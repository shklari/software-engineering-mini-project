from Domain.Cart import Cart
from .Basket import Basket


class Guest:
    def __init__(self):
        self.logged_in = False
        self.basket = Basket()
        self.creditDetails = {}  # {'type': 'visa' , 'id': 11111111 , 'credit_number': '1231123124123124'}

    # @abstractmethod # 2.6
    def add_to_cart(self, store, item, quantity):
        cart = self.basket.get_cart_by_store(store)
        if not cart:
            cart = Cart(store)
            self.basket.add_cart(cart)
        return cart.add_item_to_cart(store, item, quantity)

    # @abstractmethod # 2.7
    def get_cart(self, store_name):
        return self.basket.get_cart_by_store(store_name)

    def remove_from_cart(self, store_name, item):
        return self.basket.remove_item_from_cart(store_name, item)
