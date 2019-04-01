from Service.service import ServiceInterface
from Domain.System import System


class ServiceImpl(ServiceInterface):

    # assumes the init function receives the username and password of the system manager
    def init(self, sm_username, sm_password):
        if System.init_system(sm_username, sm_password) is not None:
            print("System initialized successfully")
            # if init_system returns the system manager object, keep it in a field???
            return True
        else:
            print("System failed to initialize")
            return False

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
        items_list = System.search(param)
        if len(items_list) == 0:
            print("No item matching the search")
            return []
        for item in items_list:
            print(item)
        return items_list

    def buy_items(self, items):
        if not System.buy_items(items):
            print("The purchase failed. The transaction is canceled")
            return False
        else:
            print("Items purchased successfully")
            return True

    def logout(self):
        if System.logout():
            print("Logged out")
            return True
        else:
            print("Logout failed")
            return False

    def create_store(self, name):
        pass

    def remove_client(self, client):
        pass

    def get_cart(self, store):
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


