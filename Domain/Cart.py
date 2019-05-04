from log.Log import Log
from Domain.Response import ResponseObject


class Cart:

    def __init__(self, store_name):
        self.store_name = store_name
        self.items_and_quantities = {}
        self.log = Log("", "")

    def add_item_to_cart(self, item_name, quantity):
        if item_name in self.items_and_quantities:
            self.items_and_quantities[item_name] += quantity
        else:
            self.items_and_quantities[item_name] = quantity
        self.log.set_info("items has been successfully added to cart", "eventLog")

    def remove_item_from_cart(self, item_name):
        if item_name in self.items_and_quantities:
            del self.items_and_quantities[item_name]
            self.log.set_info("items has been successfully removed from cart", "eventLog")
            return ResponseObject(True, True, "Item " + item_name + "has been successfully removed from cart")
        self.log.set_info("remove item fail: no such item in cart", "errorLog")
        return ResponseObject(False, False, "The item " + item_name + " doesn't exist in this cart")

    def get_store_name(self):
        return self.store_name

    def get_item_if_available(self, item_name):
        if item_name not in self.items_and_quantities:
            self.log.set_info("item is not available in store", "errorLog")
            return False
        self.items_and_quantities.get(item_name)
        return True


a = {"a": 1, "b": 30}
print(a.get("b"))

b = {'store_name': "zara"}
print()

