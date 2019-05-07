from .ExternalSystems import CollectingSystem
from .Response import ResponseObject
from log.Log import Log


class Basket:
    def __init__(self):
        self.carts = []
        self.collectingSystem = CollectingSystem()
        self.log = Log("", "")

    def get_carts(self):
        return self.carts

    def add_cart(self, cart):
        self.carts.append(cart)
        self.log.set_info("cart has been successfully added to basket", "eventLog")

    def get_cart_by_store(self, store_name):
        for cart in self.carts:
            if cart.get_store_name() == store_name:
                self.log.set_info("get cart action has succeeded", "eventLog")
                return ResponseObject(True, cart, "")
        self.log.set_info("get cart failed: no such store name", "errorLog")
        return ResponseObject(False, None, "Cart " + store_name + " doesn't exist")

    def remove_item_from_cart(self, store_name, item_name):
        result = self.get_cart_by_store(store_name)
        if not result.success:
            self.log.set_info("no such items to remove", "errorLog")
            return ResponseObject(False, False, result.message)
        cart = result.value
        removed = cart.remove_item_from_cart(item_name)
        if not removed.success:
            return removed
        self.log.set_info("items has been successfully removed from cart", "eventLog")
        return ResponseObject(True, True, "")


