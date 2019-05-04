from .ExternalSystems import CollectingSystem
from .Response import ResponseObject


class Basket:
    def __init__(self):
        self.carts = []
        self.collectingSystem = CollectingSystem()

    def get_carts(self):
        return self.carts

    def add_cart(self, cart):
        self.carts.append(cart)

    def get_cart_by_store(self, store_name):
        for cart in self.carts:
            if cart.get_store_name() == store_name:
                return ResponseObject(True, cart, "")
        return ResponseObject(False, None, "Cart " + store_name + " doesn't exist")

    def remove_item_from_cart(self, store_name, item):
        result = self.get_cart_by_store(store_name)
        if not result.success:
            return ResponseObject(False, False, "Can't remove item\n" + result.message)
        else:
            cart = result.value
            cart.remove_item_from_cart(item)
            return ResponseObject(True, True, "")


