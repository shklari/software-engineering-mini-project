from Service.service import ServiceInterface


class ServiceBridge(ServiceInterface):
    def get_cart(self, store):
        pass

    def init(self, sm_username, sm_password):
        pass

    def sign_up(self, username, password):
        pass

    def login(self, username, password):
        pass

    def search(self, param, ):
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

    def add_item_to_inventory(self, item, store, quantity):
        pass

    def remove_item_from_inventory(self, item, store, quantity):
        pass

    def edit_item_price(self, item, new_price):
        pass

    def add_new_owner(self, new_owner):
        pass

    def add_new_manager(self, new_manager):
        pass

    def set_price(self, new_price):
        pass

    def collect(self, amount, credit_details):
        pass

    def get_supply(self, user, items):
        pass
