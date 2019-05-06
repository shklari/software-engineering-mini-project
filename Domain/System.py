from Domain.ExternalSystems import *
from Domain.User import User
from Domain.Guest import Guest
from Domain.Store import Store
from Domain.Response import ResponseObject
from Domain.SystemManager import SystemManager
from passlib.hash import pbkdf2_sha256
from log.Log import Log

import functools


class System:

    def __init__(self):
        self.system_manager = None
        self.cur_user = None
        self.users = {}  # {username, user}
        self.stores = []
        self.log = Log("", "")

    def init_system(self, system_manager_user_name, system_manager_password):
        result = self.sign_up(system_manager_user_name, system_manager_password)
        if not result.success:
            self.log.set_info("System manager could not sign up", "errorLog")
            return ResponseObject(False, None, "System manager could not sign up")
        enc_password = pbkdf2_sha256.hash(system_manager_password)
        manager = SystemManager(system_manager_user_name, enc_password)
        self.users[manager.username] = manager
        self.system_manager = manager
        self.cur_user = Guest()
        return ResponseObject(True, self.cur_user, "")

    def sign_up(self, username, password):
        if username is None or username == '':
            self.log.set_info("signup failed: Username can not be empty", "errorLog")
            return ResponseObject(False, False, "Username can not be empty")
        if password is None or password == '':
            self.log.set_info("signup failed: Password can not be empty", "errorLog")
            return ResponseObject(False, False, "Password can not be empty")
        if username in self.users:
            self.log.set_info("signup failed: This user name is already taken", "errorLog")
            return ResponseObject(False, False, "This user name is already taken")
        else:
            enc_password = pbkdf2_sha256.hash(password)
            new_user = User(username, enc_password)
            self.users[username] = new_user
            self.log.set_info("signup succeeded", "eventLog")
            return ResponseObject(True, True, "Welcome new user " + username + "! You may now log in")

    def login(self, username, password):
        if username not in self.users:
            self.log.set_info("login failed: Username doesn't exist", "errorLog")
            return ResponseObject(False, False, "Username doesn't exist")
        user_to_check = self.users[username]
        if self.cur_user.logged_in:
            self.log.set_info("login failed: Someone else is logged in", "errorLog")
            return ResponseObject(False, False, "Someone else is logged in")
        if user_to_check.logged_in:
            self.log.set_info("login failed: You are already logged in", "errorLog")
            return ResponseObject(False, False, "You are already logged in")
        elif not pbkdf2_sha256.verify(password, user_to_check.password):
            self.log.set_info("login failed: Wrong password", "errorLog")
            return ResponseObject(False, False, "Wrong password")
        else:
            user_to_check.logged_in = True
            self.cur_user = user_to_check
            self.log.set_info("login succeeded", "eventLog")
            return ResponseObject(True, True, "Hey " + username + "! You are now logged in")

    def logout(self):
        if not self.cur_user.logged_in:
            self.log.set_info("logout failed: you are not logged in", "errorLog")
            return ResponseObject(False, False, "You are not logged in")
        else:
            self.cur_user.logged_in = False
            new_user = Guest()
            self.cur_user = new_user
            self.log.set_info("Logged out successfully", "eventLog")
            return ResponseObject(True, True, "Logged out successfully")

    def search(self, param):
        ret_list = []
        for store in self.stores:
            boo = store.search_item_by_name(param)
            if boo:
                ret_list.append(boo)
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

    def add_owner_to_store(self, store_name, new_owner_name):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_owner_obj = self.get_user(new_owner_name)
        if new_owner_obj is None:
            self.log.set_info("adding owner failed: user is not a user in the system", "errorLog")
            return ResponseObject(False, False, new_owner_name + " is not a user in the system")
        add = store.add_new_owner(self.cur_user, new_owner_obj)
        if not add.success:
            return add
        self.log.set_info("adding owner succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def remove_owner_from_store(self, store_name, owner_to_remove):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_owner_obj = self.get_user(owner_to_remove)
        if new_owner_obj is None:
            self.log.set_info("remove owner failed: user is not in the system", "errorLog")
            return ResponseObject(False, False, owner_to_remove + " is not a user in the system")
        remove = store.remove_owner(self.cur_user, new_owner_obj)
        if not remove.success:
            return remove
        self.log.set_info("remove owner succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def add_manager_to_store(self, store_name, new_manager_name, permissions):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_manager_obj = self.get_user(new_manager_name)
        if new_manager_obj is None:
            self.log.set_info("adding manager failed: user is not in the system", "errorLog")
            return ResponseObject(False, False, new_manager_name + " is not a user in the system")
        add = store.add_new_manager(self.cur_user, new_manager_obj, permissions)
        if not add.success:
            return add
        self.log.set_info("adding manager succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def remove_manager_from_store(self, store_name, manager_to_remove):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_manager_obj = self.get_user(manager_to_remove)
        if new_manager_obj is None:
            self.log.set_info("removing manager failed: user is not in the system", "errorLog")
            return ResponseObject(False, False, manager_to_remove + " is not a user in the system")
        remove = store.remove_manager(self.cur_user, new_manager_obj)
        if not remove.success:
            return remove
        self.log.set_info("removing manager succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def buy_items(self, items):
        # check if items exist in basket??
        supplying_system = SupplyingSystem()
        for item in items:
            if not supplying_system.get_supply(item['name']):
                self.log.set_info("buy items failed: item is out of stock", "errorLog")
                return ResponseObject(False, False, "Item " + item['name'] + " is currently out of stock")
        amount = functools.reduce(lambda acc, it: (acc + it['price']), items, 0)
        collecting_system = CollectingSystem()
        flag = collecting_system.collect(amount, self.cur_user.creditDetails)
        if not flag:
            self.log.set_info("buy items failed: payment rejected", "errorLog")
            return ResponseObject(False, False, "Payment rejected")
        for item in items:
            removed = self.cur_user.remove_from_cart(item['store_name'], item['name'])
            if not removed.success:
                self.log.set_info("buy items failed", "errorLog")
                return ResponseObject(False, False, "Cannot purchase items " + item['name'] + "\n" + removed.message)

            # Todo : remove items from store inventory
            self.log.set_info("buy items succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def create_store(self, store_name):
        if not isinstance(self.cur_user, User):
            self.log.set_info("create store failed: user is not a subscriber in the system", "errorLog")
            return ResponseObject(False, None, "You are not a subscriber in the system")
        b = False
        for stur in self.stores:
            if stur.name == store_name:
                b = True
        if b:
            self.log.set_info("create store failed: store already exists", "errorLog")
            return ResponseObject(False, None, "Store already exists")
        else:
            new_store = Store(store_name, self.cur_user)
            self.stores.append(new_store)
            self.log.set_info("create store succeeded", "eventLog")
            return ResponseObject(True, new_store, "")

    def remove_user(self, username):
        if not isinstance(self.cur_user, SystemManager):
            self.log.set_info("removing user failed: user is not a system manager", "errorLog")
            return ResponseObject(False, False, "You can't remove a user, you are not the system manager")
        if self.system_manager.username == username:
            self.log.set_info("removing user failed: user can't remove himself", "errorLog")
            return ResponseObject(False, False, "You can't remove yourself silly")
        if username not in self.users:
            self.log.set_info("removing user failed: user does not exist", "errorLog")
            return ResponseObject(False, False, "This user does not exist")
        user_to_remove = self.users[username]
        stores_to_remove = []
        for store in self.stores:
            if len(store.storeOwners) == 1 and user_to_remove.username == store.storeOwners[0].username:
                stores_to_remove.append(store)
        for st in stores_to_remove:
            self.stores.remove(st)
        del self.users[username]
        self.log.set_info("removing user succeeded", "eventLog")
        return ResponseObject(True, True, "User " + username + " removed")

    def get_store(self, store_name):
        for stor in self.stores:
            if store_name == stor.name:
                self.log.set_info("get store succeeded", "eventLog")
                return ResponseObject(True, stor, "")
        self.log.set_info("get store failed: store doesn't exist in the system", "errorLog")
        return ResponseObject(False, None, "Store " + store_name + " doesn't exist in the system")

    def get_user(self, username):
        if username in self.users:
            print(self.users[username])
            return self.users[username]
        return None

    def get_cur_user(self):
        return self.cur_user

    def add_to_cart(self, store_name, item_name, quantity):
        result = self.get_store(store_name)
        if not result.success:
            self.log.set_info("adding to cart failed: no such store", "errorLog")
            return ResponseObject(False, False, result.message)
        store = result.value
        available = store.get_item_if_available(item_name, quantity)
        if not available:
            self.log.set_info("adding to cart failed: item is not available", "errorLog")
            return ResponseObject(False, False, "Item " + item_name + "is not available")
        self.cur_user.add_to_cart(store_name, item_name, quantity)
        self.log.set_info("adding to cart succeeded", "eventLog")
        return ResponseObject(True, True, "")
