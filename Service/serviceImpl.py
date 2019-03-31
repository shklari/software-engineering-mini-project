from Service.service import ServiceInterface
from Domain.System import System


class ServiceImpl(ServiceInterface):

    def init(self, system_manager, collecting, supplying, integrity):
        pass

    def sign_up(self, username, password):
        if System.sign_up(username, password):
            print("Signed up successfully")
            return True
        else:
            print("Sign up failed")
            return False

    def login(self, username, password):
        if System.login(username, password):
            print("Logged in")
            return True
        else:
            print("Login failed. Please check username and password are correct")
            return False

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


