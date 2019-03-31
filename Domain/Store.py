

# Interface
class Store(object):

    def __init__(self, name):
        self.name = name
        # default: no rank
        self.rank = -1
        self.inventory = dict.fromkeys(['item', 'quantity'])
        self.storeOwners = []
        self.storeManagers = []

    # 4.1.1
    def add_item_to_inventory(self, user, item, quantity): pass

    # 4.1.2
    def remove_item_from_inventory(self, user, item, quantity): pass

    # 4.1.3
    def edit_item_price(self, item, new_price): pass

    def set_policy(self, new_policy): pass

    # 4.3
    def add_new_owner(self, owner, new_owner): pass

    # 4.4
    def remove_owner(self, owner, owner_to_remove): pass

    # 4.5
    def add_new_manager(self, owner, new_manager): pass

    # 4.6
    def remove_manager(self, owner, manager_to_remove): pass

    def search_item_by_name(self, item_name):
        result_list = []
        for item in self.inventory.keys():
            if item.name == item_name:
                result_list += item
        return result_list

    def search_item_by_price(self, price):
        result_list = []
        for item in self.inventory.keys():
            if item.price == price:
                result_list += item
        return result_list

    def search_item_by_category(self, category):
        result_list = []
        for item in self.inventory.keys():
            if item.category == category:
                result_list += item
        return result_list
