from Domain.System import System


class Cart:

    def __init__(self, store_name):
        self.store_name = store_name
        self.items_and_quantities = {}

    def add_item_to_cart(self, item_name, quantity):
        if not self.get_item_if_available(item_name):
            return False
        if item_name in self.items_and_quantities:
            self.items_and_quantities[item_name] += quantity
        else:
            self.items_and_quantities[item_name] = quantity
        return True

    def get_item_if_available(self, item_name):
        my_store = System.get_store(self.store_name)
        bol = False
        for k in my_store.inventory:
            if k['name'] == my_store.name:
                if k['quantity'] > 0:
                    bol = True
        if my_store.search_item_by_name(item_name) and bol:
            return my_store.search_item_by_name(item_name)
        return False

    def remove_item_from_cart(self, item_name):
        if item_name in self.items_and_quantities:
            del self.items_and_quantities[item_name]
            return True
        return False

    def get_store_name(self):
        return self.store_name
