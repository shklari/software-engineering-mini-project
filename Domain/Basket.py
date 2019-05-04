from .ExternalSystems import CollectingSystem


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
                return cart
        return False

    def remove_item_from_cart(self, store_name, item):
        cart = self.get_cart_by_store(store_name)
        cart.remove_item_from_cart(item)


