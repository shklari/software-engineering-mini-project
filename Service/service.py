from abc import abstractmethod


# Interface


class SystemInterface(object):

    @abstractmethod # 1.1 ?????
    def init(self, system_manager, collecting, supplying, integrity): pass

    @abstractmethod # 2.2
    def sign_up(self, username, password): pass

    @abstractmethod # 2.3
    def login(self, username, password): pass

    @abstractmethod # 2.4
    def search(self, param): pass

    @abstractmethod # 2.8
    def buy_items(self, items): pass

    @abstractmethod # 3.1
    def logout(self): pass

    @abstractmethod # 3.2
    def create_store(self, name): pass

    @abstractmethod # 6.2
    def remove_client(self, client): pass

    @abstractmethod # 2.6
    def add_to_cart(self, store, items): pass

    @abstractmethod # 2.7
    def edit_cart(self, cart, params): pass

    @abstractmethod # 2.8
    def buy_item(self, item): pass

    @abstractmethod # 2.8
    def remove_owner(self, owner): pass

    @abstractmethod # 2.8
    def remove_manager(self, manager): pass

    @abstractmethod # 4.1.1
    def add_item_to_inventory(self, user, item, quantity): pass

    @abstractmethod # 4.1.2
    def remove_item_from_inventory(self, user, item, quantity): pass

    @abstractmethod # 4.1.3
    def edit_item_price(self, item, new_price): pass

    @abstractmethod # 4.3
    def add_new_owner(self, owner, new_owner): pass

    @abstractmethod # 4.4
    def remove_owner(self, owner, owner_to_remove): pass

    @abstractmethod # 4.5
    def add_new_manager(self, owner, new_manager): pass

    @abstractmethod # 4.6
    def remove_manager(self, owner, manager_to_remove): pass

    @abstractmethod # 4.1.3
    def set_price(self, new_price): pass

    @abstractmethod # 7 ?????
    def collect(self, amount, credit_details): pass

    @abstractmethod # 8 ?????
    def get_supply(self, user, items): pass
