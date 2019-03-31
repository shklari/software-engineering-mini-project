from Service.service import SystemInterface

class CollectingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True


class SupplyingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True


class IntegritySystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True


class ServiceBridge(SystemInterface):
    def init(self, system_manager, collecting, supplying, integrity):
        pass

    def sign_up(self, username, password):
        pass

    def login(self, username, password):
        pass

    def search(self, param):
        pass

    def buy_items(self, items):
        pass

    def logout(self):
        pass

    def create_store(self, name):
        pass

    def remove_client(self, client):
        pass

    def add_to_cart(self, store, items):
        pass

    def edit_cart(self, cart, params):
        pass

    def buy_item(self, item):
        pass

    def remove_owner(self, owner):
        pass

    def remove_manager(self, manager):
        pass

    def add_item_to_inventory(self, user, item, quantity):
        pass

    def remove_item_from_inventory(self, user, item, quantity):
        pass

    def edit_item_price(self, item, new_price):
        pass

    def add_new_owner(self, owner, new_owner):
        pass

    def add_new_manager(self, owner, new_manager):
        pass

    def set_price(self, new_price):
        pass

    def collect(self, amount, credit_details):
        pass

    def get_supply(self, user, items):
        pass