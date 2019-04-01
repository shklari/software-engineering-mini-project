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

    def search(self, keyword):
        items_list = System.search(keyword)
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
        created = System.create_store(name)
        if not created:
            print("Could not create store" + name)
            return False
        else:
            print("New store created")
            print("Name: " + created.name)
            print("Owners: " + created.storeOwners)
            owners = []
            for o in created.storeOwners:
                owners.append({'username': o.username})
            return {'name': created.name, 'storeOwners': owners}

    def remove_user(self, username):
        if not System.remove_user(username):
            print("Can't remove user")
            return False
        else:
            print("User " + username + "removed")
            return True

    def get_cart(self, store_name):
        pass

    def get_item_from_cart(self, cart, item):
        pass

    def add_to_cart(self, store_name, items):
        pass

    def remove_from_cart(self, store_name, item):
        pass

    def buy_item(self, item):
        pass

    def remove_owner(self, owner):
        pass

    def remove_manager(self, manager):
        pass

    def add_item_to_inventory(self, user, store_name, item, quantity):
        store = System.get_store(store_name)
        if store is None:
            print("Error: can't add items to store " + store_name)
            return False
        if not store.add_item_to_inventory(user, item, quantity):
            print("Error: can't add item " + item + " to store " + store_name)
            return False
        return {'name': store.name, 'inventory': store.inventory}

    def remove_item_from_inventory(self, user, store_name, item, quantity):
        store = System.get_store(store_name)
        if store is None:
            print("Error: can't remove items from store " + store_name)
            return False
        if not store.remove_item_from_inventory(user, item, quantity):
            print("Error: can't remove item " + item + " to store " + store_name)
            return False
        return {'name': store.name, 'inventory': store.inventory}

    def edit_item_price(self, user, store_name, item, new_price):
        store = System.get_store(store_name)
        if store is None:
            print("Error: can't edit items in store " + store_name)
            return False
        if not store.edit_item_price(user, item, new_price):
            print("Error: can't edit item " + item + " in store " + store_name)
            return False
        # complete!!

    def add_new_owner(self, new_owner):
        pass

    def add_new_manager(self, new_manager):
        pass

    def set_price(self, new_price):
        pass


