from .User import User
from .Client import Client
from .Store import Store
from .StoreOwner import StoreOwner
from .SystemManager import SystemManager


class System:

    def __init__(self, system_manager):
        self.sys_manager = system_manager
        self.cur_user = User()
        self.clients = dict.fromkeys(['username', 'client'])
        self.stores = []

    def sign_up(self, username, password):
        if self.clients[username] is not None:
            print("This user name is taken")
            return False
        if password is None:
            print("Password can not be empty")
            return False
        else:
            new_client = Client(username, password)
            self.clients[username] = new_client
            return True

    def login(self, username, password):
        client_to_check = self.clients[username]
        if client_to_check is None:
            print("No such user")
            return False
        if client_to_check.logged_in:
            print("You are already logged in")
            return False
        elif client_to_check.password != password:
            print("Wrong password")
            return False
        else:
            client_to_check.logged_in = True
            self.cur_user = client_to_check
            return client_to_check

    def logout(self):
        if not self.cur_user.logged_in:
            print("You can't log out until you log in")
            return False
        else:
            self.cur_user.logged_in = False
            new_user = User()
            self.cur_user = new_user
            return new_user

    def search(self, param):
        ret_list = []
        for s in self.stores:
            ret_list += s.search_item_by_name(param)
            ret_list += s.search_item_by_category(param)
            ret_list += s.search_item_by_price(param)

        return ret_list

    def filter_by_price_range(self, item_list, low, high):
        result_list = []
        for item in item_list:
            if low <= item.price <= high:
                result_list += item
        return result_list

    def filter_by_item_rank(self, item_list, low, high):
        result_list = []
        for item in item_list:
            if low <= item.rank <= high:
                result_list += item
        return result_list

    def filter_by_item_category(self, item_list, category):
        result_list = []
        for item in item_list:
            if item.category == category:
                result_list += item
        return result_list

    def buy_items(self, items):
        flag = False
        for item in items:
            flag = self.cur_user.buy_item(item)
        return flag

    def create_store(self, name):
        new_owner = self.cur_user
        if new_owner.logged_in and name not in self.stores:
            new_store = Store(name)
            if not isinstance(new_owner, StoreOwner):
                new_owner = StoreOwner(self.cur_user.username, self.cur_user.password)
            new_store.storeOwners.append(new_owner)
            self.stores += new_store
            return new_store
        return False

    def remove_client(self, client_name):
        if not isinstance(self.cur_user, SystemManager):
            print("You can't remove a client, you are not the system manager")
            return False
        client_to_remove = self.clients[client_name]
        for store in self.stores:
            if client_to_remove in store.storeOwners and len(store.storeOwners) == 1:
                self.stors.remove(store)
        del self.clients[client_to_remove]
        return True
