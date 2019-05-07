from Domain.Cart import Cart
from .Basket import Basket
from log.Log import Log


class Guest:
    def __init__(self):
        self.logged_in = False
        self.basket = Basket()
        self.creditDetails = {}  # {'type': 'visa' , 'id': 11111111 , 'credit_number': '1231123124123124'}
        self.log = Log("", "")

    # @abstractmethod # 2.6
    def add_to_cart(self, store_name, item_name, quantity):
        result = self.basket.get_cart_by_store(store_name)
        cart = result.value
        if not result.success:
            cart = Cart(store_name)
            self.basket.add_cart(cart)
        cart.add_item_to_cart(item_name, quantity)
        self.log.set_info("item has been successfully added to cart", "eventLog")

    # @abstractmethod # 2.7
    def get_cart(self, store_name):
        return self.basket.get_cart_by_store(store_name)

    def remove_from_cart(self, store_name, item_name):
        return self.basket.remove_item_from_cart(store_name, item_name)
