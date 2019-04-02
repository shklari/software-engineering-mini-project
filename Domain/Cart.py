from Domain.System import System


class Cart:

    def __init__(self, store_name):
        self.store_name = store_name
        self.items_and_quantities = {}

    def add_item_to_cart(self, store, item_name, quantity):
        if not self.get_item_if_available(item_name, store):
            return False
        if item_name in self.items_and_quantities:
            self.items_and_quantities[item_name] += quantity
        else:
            self.items_and_quantities[item_name] = quantity
        return True

    def get_item_if_available(self, item_name, store):
        if item_name in store.inventory and store.inventory[item_name] > 0:
            return store.inventory[item_name]
        return False

    def remove_item_from_cart(self, item_name):
        if item_name in self.items_and_quantities:
            del self.items_and_quantities[item_name]
            return True
        return False

    def get_store_name(self):
        return self.store_name
