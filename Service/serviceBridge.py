from Service.service import ServiceInterface
from Service.serviceImpl import ServiceImpl


class ServiceBridge(ServiceInterface):
    real = None

    def __init__(self):
        self.real = ServiceImpl()

    def get_item_from_cart(self, cart, item_name):
        pass

    def remove_user(self, username):
        return True if self.real is None else self.real.remove_user(username)

    def get_cart(self, store):
        return True if self.real is None else self.real.get_cart(store)

    def init(self, sm_username, sm_password):
        return True if self.real is None else self.real.init(sm_username, sm_password)

    def sign_up(self, username, password):
        return True if self.real is None else self.real.sign_up(username, password)

    def login(self, username, password):
        return True if self.real is None else self.real.login(username, password)

    def search(self, param):
        return True if self.real is None else self.real.search(param)

    def buy_items(self, items):
        return True if self.real is None else self.real.buy_items(items)

    def logout(self):
        return True if self.real is None else self.real.logout()

    def create_store(self, name):
        return True if self.real is None else self.real.create_store(name)

    def add_to_cart(self, store_name, item_name, quantity):
        return True if self.real is None else self.real.add_to_cart(store_name, item_name, quantity)

    def remove_from_cart(self, storename, item):
        return True if self.real is None else self.real.remove_from_cart(storename, item)

    def buy_item(self, item):
        return True if self.real is None else self.real.buy_item(item)

    def remove_owner(self, storename, ownertoremove):
        return True if self.real is None else self.real.remove_owner(storename, ownertoremove)

    def remove_manager(self, store_name, manager_to_remove):
        return True if self.real is None else self.real.remove_manager(store_name, manager_to_remove)

    def add_item_to_inventory(self, item, store, quantity):
        return True if self.real is None else self.real.add_item_to_inventory(item, store, quantity)

    def remove_item_from_inventory(self, item, store, quantity):
        return True if self.real is None else self.real.remove_item_from_inventory(item, store, quantity)

    def edit_item_price(self, item, store_name, new_price):
        return True if self.real is None else self.real.edit_item_price(item, store_name, new_price)

    def add_new_owner(self, store_name, new_owner):
        return True if self.real is None else self.real.add_new_owner(store_name, new_owner)

    def add_new_manager(self, store_name, new_manager, permission):
        return True if self.real is None else self.real.add_new_manager(store_name, new_manager, permission)

