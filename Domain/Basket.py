from .CollectingSystem import CollectingSystem


class Basket:
    def __init__(self):
        self.carts = []
        self.collectingSystem = CollectingSystem()

    def get_carts(self):
        return self.carts

    def get_cart_by_store(self, storeNmae):
        for cart in self.carts:
            if cart.get_store_name() == storeNmae: return cart
        return False

    def remove_item_from_cart(self, storeNmae, item):
        cart = self.get_cart_by_store(storeNmae)
        cart.remove_item_from_cart(item)


