from Domain.System import System


class Cart:

    def __init__(self, store_name):
        self.store = System.get_store(store_name)
        self.item_list = []

    def add_item_to_cart(self, item):
        if item not in self.item_list:
            self.item_list.append(item)
            return True
        return False

    def get_items(self):
        return self.item_list

    def remove_item_from_cart(self, item):
        if item in self.item_list:
            self.item_list.remove(item)
            return True
        return False
