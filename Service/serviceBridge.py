from Service.service import ServiceInterface
from Service.serviceImpl import ServiceImpl


class ServiceBridge(ServiceInterface):
    real = None

    def __init__(self):
        self.real = ServiceImpl()

    def remove_from_cart(self, store_name, item):
        pass

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

    def remove_user(self, user):
        return True if self.real is None else self.real.remove_client(user)

    def add_to_cart(self, store, items):
        return True if self.real is None else self.real.add_to_cart(store, items)

    def edit_cart(self, cart, params):
        return True if self.real is None else self.real.edit_cart(cart, params)

    def buy_item(self, item):
        return True if self.real is None else self.real.buy_item(item)

    def remove_owner(self, owner):
        return True if self.real is None else self.real.remove_owner(owner)

    def remove_manager(self, manager):
        return True if self.real is None else self.real.remove_manager(manager)

    def add_item_to_inventory(self, item, store, quantity):
        return True if self.real is None else self.real.add_item_to_inventory(item, store, quantity)

    def remove_item_from_inventory(self, item, store, quantity):
        return True if self.real is None else self.real.remove_item_from_inventory(item, store, quantity)

    def edit_item_price(self, item, new_price):
        return True if self.real is None else self.real.edit_item_price(item, new_price)

    def add_new_owner(self, new_owner):
        return True if self.real is None else self.real.add_new_owner(new_owner)

    def add_new_manager(self, new_manager):
        return True if self.real is None else self.real.add_new_manager(new_manager)

    def set_price(self, new_price):
        return True if self.real is None else self.real.set_price(new_price)

    def collect(self, amount, credit_details):
        return True if self.real is None else self.real.collect(amount, credit_details)

    def get_supply(self, user, items):
        return True if self.real is None else self.real.get_supply(user, items)
