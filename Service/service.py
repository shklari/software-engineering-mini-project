from abc import abstractmethod

# Interface

# store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
# item {'name', 'price', 'category'}
# user {'username'}
# cart {'store_name', 'items': []}


class ServiceInterface(object):

    @abstractmethod  # 1.1 username, password are strings
    def init(self, sm_username, sm_password): pass

    @abstractmethod  # 2.2 username, password are strings
    def sign_up(self, username, password): pass

    @abstractmethod  # 2.3 username, password are strings
    def login(self, username, password): pass

    @abstractmethod  # 2.4 keyword is string
    def search(self, keyword): pass

    @abstractmethod  # 2.8 items is a list of item dictionaries
    def buy_items(self, items): pass

    @abstractmethod  # 3.1
    def logout(self): pass

    @abstractmethod  # 3.2 name is string
    def create_store(self, name): pass

    @abstractmethod  # 6.2 username is string
    def remove_user(self, username): pass

    @abstractmethod  # 2.7 store_name is string
    def get_cart(self, store_name): pass

    @abstractmethod  # cart is cart dictionary, item_name is string
    def get_item_from_cart(self, cart, item_name):
        pass

    @abstractmethod  # 2.6 store_name is string
    def add_to_cart(self, store_name, item): pass

    @abstractmethod  # 2.7 store_name is string
    def remove_from_cart(self, store_name, item): pass

    @abstractmethod  # 2.8 item is item dictionary
    def buy_item(self, item): pass

    @abstractmethod  # 4.1.1 item is item dictionary, store_name is string
    def add_item_to_inventory(self, item, store_name, quantity): pass

    @abstractmethod  # 4.1.2 item is item dictionary, store_name is string
    def remove_item_from_inventory(self, item, store_name, quantity): pass

    @abstractmethod  # 4.1.3
    def edit_item_price(self, store_name, item, new_price): pass

    @abstractmethod  # 4.3
    def add_new_owner(self, store_name, new_owner): pass

    @abstractmethod  # 4.4
    def remove_owner(self, store_name, owner_to_remove): pass

    @abstractmethod  # 4.5
    def add_new_manager(self, store_name, new_manager): pass

    @abstractmethod  # 4.6
    def remove_manager(self, store_name, manager_to_remove): pass

