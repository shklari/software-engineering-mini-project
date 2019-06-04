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
        self.supplying_system = SupplyingSystem()
        self.collecting_system = CollectingSystem()
        self.traceability_system = TraceabilitySystem()

    def init_system(self, system_manager_user_name, system_manager_password):
        if not self.supplying_system.init() or not self.traceability_system.init() or self.collecting_system.init():
            ret = False
        else:
            ret = True
        result = self.sign_up(system_manager_user_name, system_manager_password)
        if not result.success:
            self.log.set_info("error: System manager could not sign up", "eventLog")
            return ResponseObject(False, None, "System manager could not sign up")
        enc_password = pbkdf2_sha256.hash(system_manager_password)
        manager = SystemManager(system_manager_user_name, enc_password)
        self.users[manager.username] = manager
        self.system_manager = manager
        self.cur_user = Guest()
        return ResponseObject(ret, self.cur_user, "")

    def sign_up(self, username, password):
        if username is None or username == '':
            self.log.set_info("error: signup failed: Username can not be empty", "eventLog")
            return ResponseObject(False, False, "Username can not be empty")
        if password is None or password == '':
            self.log.set_info("error: signup failed: Password can not be empty", "eventLog")
            return ResponseObject(False, False, "Password can not be empty")
        if username in self.users:
            self.log.set_info("error: signup failed: This user name is already taken", "eventLog")
            return ResponseObject(False, False, "This user name is already taken")
        else:
            enc_password = pbkdf2_sha256.hash(password)
            new_user = User(username, enc_password)
            self.users[username] = new_user
            self.log.set_info("signup succeeded", "eventLog")
            return ResponseObject(True, True, "Welcome new user " + username + "! You may now log in")

    def login(self, username, password):
        if username not in self.users:
            self.log.set_info("error: login failed: Username doesn't exist", "eventLog")
            return ResponseObject(False, False, "Username doesn't exist")
        user_to_check = self.users[username]
        if self.cur_user.logged_in:
            self.log.set_info("error: login failed: Someone else is logged in", "eventLog")
            return ResponseObject(False, False, "Someone else is logged in")
        if user_to_check.logged_in:
            self.log.set_info("error: login failed: You are already logged in", "eventLog")
            return ResponseObject(False, False, "You are already logged in")
        elif not pbkdf2_sha256.verify(password, user_to_check.password):
            self.log.set_info("error: login failed: Wrong password", "eventLog")
            return ResponseObject(False, False, "Wrong password")
        else:
            user_to_check.logged_in = True
            self.cur_user = user_to_check
            self.log.set_info("login succeeded", "eventLog")
            return ResponseObject(True, True, "Hey " + username + "! You are now logged in")

    def logout(self):
        if not self.cur_user.logged_in:
            self.log.set_info("error: logout failed: you are not logged in", "eventLog")
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
            self.log.set_info("error: adding owner failed: user is not a user in the system", "eventLog")
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
            self.log.set_info("error: remove owner failed: user is not in the system", "eventLog")
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
            self.log.set_info("error: adding manager failed: user is not in the system", "eventLog")
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
            self.log.set_info("error: removing manager failed: user is not in the system", "eventLog")
            return ResponseObject(False, False, manager_to_remove + " is not a user in the system")
        remove = store.remove_manager(self.cur_user, new_manager_obj)
        if not remove.success:
            return remove
        self.log.set_info("removing manager succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def buy_items(self, items):
        # check if items exist in basket??
        if not self.get_cur_user().buying_policy.apply_policy():
            self.log.set_info("error: buy items failed: user policy", "eventLog")
            return ResponseObject(False, False, "buy items failed: User " + self.cur_user + " policy")
        for item in items:
            store = self.get_store(item['store_name'])
            if not store.success:
                self.log.set_info("error: buy items failed: store does not exist", "eventLog")
                return ResponseObject(False, False, "buy items failed: Store " + item['store_name'] + " does not exist")
            if not store.value.policy.apply_policy():
                self.log.set_info("error: buy items failed: store policy", "eventLog")
                return ResponseObject(False, False, "buy items failed: Store " + item['store_name'] + " policy")
            tmp_item = store.value.search_item_by_name(item['name'])
            if not tmp_item:
                self.log.set_info("error: buy items failed: item is not in store's inventory", "eventLog")
                return ResponseObject(False, False, "buy items failed: Item " + item['name'] + " is not in "
                                      + item['store_name'])
            if not tmp_item.buying_policy.apply_policy():
                self.log.set_info("error: buy items failed: item policy", "eventLog")
                return ResponseObject(False, False, "Item " + item['name'] + "'s policy isn't allowing buying it")
            if not self.supplying_system.get_supply(item['name']):
                self.log.set_info("error: buy items failed: item is out of stock", "eventLog")
                return ResponseObject(False, False, "Item " + item['name'] + " is currently out of stock")
        # TODO: apply discount
        amount = functools.reduce(lambda acc, it: (acc + it['price']), items, 0)
        flag = self.collecting_system.collect(amount, self.cur_user.creditDetails)
        if not flag:
            self.log.set_info("error: buy items failed: payment rejected", "eventLog")
            return ResponseObject(False, False, "Payment rejected")
        for item in items:
            removed = self.cur_user.remove_from_cart(item['store_name'], item['name'])
            if not removed.success:
                self.log.set_info("error: buy items failed", "eventLog")
                return ResponseObject(False, False, "Cannot purchase item " + item['name'] + "\n" + removed.message)

        # Todo : remove items from store inventory
        self.log.set_info("buy items succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def create_store(self, store_name):
        if not isinstance(self.cur_user, User):
            self.log.set_info("error: create store failed: user is not a subscriber in the system", "eventLog")
            return ResponseObject(False, None, "You are not a subscriber in the system")
        b = False
        for stur in self.stores:
            if stur.name == store_name:
                b = True
        if b:
            self.log.set_info("error: create store failed: store already exists", "eventLog")
            return ResponseObject(False, None, "Store already exists")
        else:
            new_store = Store(store_name, self.cur_user)
            self.stores.append(new_store)
            self.log.set_info("create store succeeded", "eventLog")
            return ResponseObject(True, new_store, "")

    def remove_user(self, username):
        if not isinstance(self.cur_user, SystemManager):
            self.log.set_info("error: removing user failed: user is not a system manager", "eventLog")
            return ResponseObject(False, False, "You can't remove a user, you are not the system manager")
        if self.system_manager.username == username:
            self.log.set_info("error: removing user failed: user can't remove himself", "eventLog")
            return ResponseObject(False, False, "You can't remove yourself silly")
        if username not in self.users:
            self.log.set_info("error: removing user failed: user does not exist", "eventLog")
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
        self.log.set_info("error: get store failed: store doesn't exist in the system", "eventLog")
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
            self.log.set_info("error: adding to cart failed: no such store", "eventLog")
            return ResponseObject(False, False, result.message)
        store = result.value
        available = store.get_item_if_available(item_name, quantity)
        if not available:
            self.log.set_info("error: adding to cart failed: item is not available", "eventLog")
            return ResponseObject(False, False, "Item " + item_name + "is not available")
        self.cur_user.add_to_cart(store_name, item_name, quantity)
        self.log.set_info("adding to cart succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def get_total_system_inventory(self):
        retList = []
        for stur in self.stores:
            retList.extend(stur.inventory)
        return ResponseObject(True, retList, "")
