

class Cart:

    def __init__(self, store_name):
        self.store_name = store_name
        self.items_and_quantities = {}

    def add_item_to_cart(self, item_name, quantity):
        if item_name in self.items_and_quantities:
            self.items_and_quantities[item_name] += quantity
        else:
            self.items_and_quantities[item_name] = quantity
        return True

    def remove_item_from_cart(self, item_name):
        if item_name in self.items_and_quantities:
            del self.items_and_quantities[item_name]
            return True
        return False

    def get_store_name(self):
        return self.store_name

    def get_item_if_available(self, item_name):
        if item_name not in self.items_and_quantities:
            print("item is not available in store")
            return False
        self.items_and_quantities.get(item_name)
        return True
