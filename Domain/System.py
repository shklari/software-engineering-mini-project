from Domain.CollectingSystem import CollectingSystem
from Domain.User import User
from Domain.Guest import Guest
from Domain.Store import Store
from Domain.StoreOwner import StoreOwner
from Domain.SystemManager import SystemManager
from passlib.hash import pbkdf2_sha256

import functools


class System:

    def __init__(self):
        self.system_manager = 0
        self.cur_user = 0
        self.users = {}
        self.stores = []

    def init_system(self, system_manager_user_name, system_manager_password):
        if not self.sign_up(system_manager_user_name, system_manager_password):
            return None
        enc_password = pbkdf2_sha256.hash(system_manager_password)
        manager = SystemManager(system_manager_user_name, enc_password)
        self.users[manager.username] = manager
        self.system_manager = manager
        self.cur_user = Guest()
        return self.cur_user

    def sign_up(self, username, password):
        if username is None or username == '':
            print("Username can not be empty")
            return False
        if password is None or password == '':
            print("Password can not be empty")
            return False
        if username in self.users:
            print("This user name is taken")
            return False
        else:
            enc_password = pbkdf2_sha256.hash(password)
            new_user = User(username, enc_password)
            self.users[username] = new_user
            print("Welcome, new user {}! You may now log in".format(username))
            return True

    def login(self, username, password):
        if username not in self.users:
            print("No such user")
            return False
        user_to_check = self.users[username]
        if self.cur_user.logged_in:
            print("Someone else is logged in")
            return False
        if user_to_check.logged_in:
            print("You are already logged in")
            return False
        elif not pbkdf2_sha256.verify(password, user_to_check.password):
            print("Wrong password")
            return False
        else:
            user_to_check.logged_in = True
            self.cur_user = user_to_check
            print("Hey {}! You are now logged in".format(username))
            return True

    def logout(self):
        if not self.cur_user.logged_in:
            print("You can't log out until you log in")
            return False
        else:
            self.cur_user.logged_in = False
            new_user = Guest()
            self.cur_user = new_user
            print("You are now logged out")
            return True

    def search(self, param):
        ret_list = []
        for store in self.stores:
            boo = store.search_item_by_name(param)
            if boo:
                ret_list.append(store.search_item_by_name(param))
            ret_list.extend(store.search_item_by_category(param))
            ret_list.extend(store.search_item_by_price(param))
        return ret_list

    @staticmethod
    def filter_by_price_range(item_list, low, high):
        result_list = []
        for item in item_list:
            if low <= item.price <= high:
                result_list.append(item)
        return result_list

    @staticmethod
    def filter_by_item_rank(item_list, low, high):
        result_list = []
        for item in item_list:
            if low <= item.rank <= high:
                result_list.append(item)
        return result_list

    @staticmethod
    def filter_by_item_category(item_list, category):
        result_list = []
        for item in item_list:
            if item.category == category:
                result_list.append(item)
        return result_list

    def add_owner_to_store(self, store_name, new_owner):
        store = self.get_store(store_name)
        if store is None:
            return False
        new_owner_obj = self.get_user(new_owner)
        return False if new_owner_obj is None else store.add_new_owner(self.cur_user, new_owner_obj)

    def remove_owner_from_store(self, store_name, owner_to_remove):
        store = self.get_store(store_name)
        if store is None:
            return False
        new_owner_obj = self.get_user(owner_to_remove)
        return False if new_owner_obj is None else store.remove_owner(self.cur_user, new_owner_obj)

    def add_manager_to_store(self, store_name, new_manager, permissions):
        store = self.get_store(store_name)
        if store is None:
            return False
        new_manager_obj = self.get_user(new_manager)
        return False if new_manager_obj is None else store.add_new_manager(self.cur_user, new_manager_obj, permissions)

    def remove_manager_from_store(self, store_name, manager_to_remove):
        store = self.get_store(store_name)
        if store is None:
            return False
        new_manager_obj = self.get_user(manager_to_remove)
        return False if new_manager_obj is None else store.remove_manager(self.cur_user, new_manager_obj)

    def buy_items(self, items): # fixed by yosi
        amount = functools.reduce(lambda acc, item: (acc + item.price), items, 0)
        collecting_system = CollectingSystem()
        flag = collecting_system.collect(amount, self.cur_user.creditDetails)
        for item in items:
            flag = self.cur_user.remove_from_cart(item.store_name, item)
        return flag

    def create_store(self, store_name):
        b = False
        for stur in self.stores:
            if stur.name == store_name:
                b = True
        if isinstance(self.cur_user, User) and not b:
            new_store = Store(store_name, self.cur_user)
            self.stores.append(new_store)
            return new_store
        return False

    def remove_user(self, username):
        if not isinstance(self.cur_user, SystemManager):
            print("You can't remove a user, you are not the system manager")
            return False
        if self.system_manager.username == username:
            print("You can't remove yourself silly")
            return False
        if username not in self.users:
            print("This user does not exist")
            return False
        user_to_remove = self.users[username]
        stores_to_remove = []
        for store in self.stores:
            if len(store.storeOwners) == 1 and user_to_remove.username == store.storeOwners[0].username:
                stores_to_remove.append(store)
        for st in stores_to_remove:
            self.stores.remove(st)
        del self.users[username]
        print("System manager removed the user {}".format(username))
        return True

    def get_store(self, store_name):
        for stor in self.stores:
            if store_name == stor.name:
                return stor
        return None

    def get_user(self, username):
        if username in self.users:
            print(self.users[username])
            return self.users[username]
        return None

    def get_cur_user(self):
        return self.cur_user
