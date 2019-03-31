from Service.service import ServiceInterface


class ServiceImpl(ServiceInterface):

    def init(self, system_manager, collecting, supplying, integrity):
        pass

    def sign_up(self, username, password):
        pass

    def login(self, username, password):
        pass

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
            print("Can't logout")
            return False

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


