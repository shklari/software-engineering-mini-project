from django.utils.datetime_safe import datetime

from Domain.Cart import Cart
from Domain.StoreOwner import StoreOwner
from Domain.User import User
from Domain.Guest import Guest
from Domain.Store import Store
from Domain.Response import ResponseObject
from Domain.SystemManager import SystemManager
from passlib.hash import pbkdf2_sha256
from log.Log import Log
from DataAccess.mongoDB import DB
import functools
from Domain.BuyingPolicy import *
from Domain.SupplyingSystem import SupplyingSystem
from Domain.CollectingSystem import CollectingSystem


class System:

    def __init__(self):
        self.user_types = {"1": "guest", "2": "user", "3": "store_owner", "4": "store_manager", "5": "sys_manager"}
        self.system_manager = None
        self.database = DB()
        # self.users = {}  # {username, user}
        self.loggedInUsers = {}     # logged in users that are currently in the system
        self.guests = {}    # guests that are currently in the system
        self.stores = []
        self.log = Log("", "")
        self.supplying_system = SupplyingSystem()
        self.collecting_system = CollectingSystem()
        # self.traceability_system = TraceabilitySystem()

    def get_user_or_guest(self, username):
        if username in self.loggedInUsers:
            curr_user = self.loggedInUsers[username]
        elif username in self.guests:
            curr_user = self.guests[username]
        else:
            return ResponseObject(False, False, "User " + username + " doesn't exist in the system")
        return ResponseObject(True, curr_user, "")

    # guest_id is IP and port
    def new_guest(self, guest_id):
        self.guests[guest_id] = Guest()

    def init_system(self, system_manager_user_name, system_manager_password, system_manager_age, system_manager_country):
        if not self.supplying_system.supply_handshake() or not self.collecting_system.collect_handshake():
            return ResponseObject(False, False, "Can't init external systems")
        result=''
        if not self.get_user(system_manager_user_name):
            result = self.sign_up(system_manager_user_name, system_manager_password, system_manager_age,system_manager_country)
            if not result.success:
                self.log.set_info("error: System manager could not sign up", "eventLog")
                return ResponseObject(False, None, "System manager could not sign up")
        enc_password = pbkdf2_sha256.hash(system_manager_password)
        manager = SystemManager(system_manager_user_name, enc_password, system_manager_age, system_manager_country)
        self.database.add_user(manager)
        # self.users[manager.username] = manager
        self.system_manager = manager
        self.stores = self.database.get_all_stores()
        return ResponseObject(True, True, "")

    def sign_up(self, username, password, age, country):
        if username is None or username == '':
            self.log.set_info("error: signup failed: Username can not be empty", "eventLog")
            return ResponseObject(False, False, "Username can not be empty")
        if password is None or password == '':
            self.log.set_info("error: signup failed: Password can not be empty", "eventLog")
            return ResponseObject(False, False, "Password can not be empty")
        # if username in self.users:
        if self.does_user_exist_in_db(username):
            self.log.set_info("error: signup failed: This user name is already taken", "eventLog")
            return ResponseObject(False, False, "This user name is already taken")
        else:
            enc_password = pbkdf2_sha256.hash(password)
            new_user = User(username, enc_password, age, country)
            self.database.add_user(new_user)
            # self.users[username] = new_user
            self.log.set_info("signup succeeded", "eventLog")
            return ResponseObject(True, True, "Welcome new user " + username + "! You may now log in")

    def login(self, username, password):
        # if username not in self.users:
        if not self.does_user_exist_in_db(username):
            self.log.set_info("error: login failed: Username doesn't exist", "eventLog")
            return ResponseObject(False, False, "Username doesn't exist")
        # user_to_check = self.users[username]
        user_to_check = self.get_user(username)
        if user_to_check.logged_in:
            self.log.set_info("error: login failed: You are already logged in", "eventLog")
            return ResponseObject(False, False, "You are already logged in")
        elif not pbkdf2_sha256.verify(password, user_to_check.password):
            self.log.set_info("error: login failed: Wrong password", "eventLog")
            return ResponseObject(False, False, "Wrong password")
        else:
            user_to_check.logged_in = True
            self.loggedInUsers[username] = user_to_check
            self.log.set_info("login succeeded", "eventLog")
            user_type = self.get_user_type(username)
            return ResponseObject(True, user_type, "Hey " + username + "! You are now logged in")

    def logout(self, username):
        if username not in self.loggedInUsers:
            self.log.set_info("error: logout failed: you are not logged in", "eventLog")
            return ResponseObject(False, False, "You are not logged in")
        else:
            self.loggedInUsers[username].logged_in = False
            self.loggedInUsers.pop(username)
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

    def add_owner_to_store(self, store_name, new_owner_name, username):
        new_owner_obj = self.get_user(new_owner_name)
        # check if this user is sign in #
        if new_owner_obj is None:
            self.log.set_info("error: adding owner failed: user is not a user in the system", "eventLog")
            return ResponseObject(False, False, new_owner_name + " is not a user in the system")
        #
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        # add supporting in vote requirement in version 3

        owner_list = store.storeOwners
        # check if username is owner #
        found = False
        for owner in owner_list:
            if owner.username == username:
                found = True
                break
        if not found:
            return ResponseObject(False, False, username + " is not a owner of this store!")
        #
        if len(owner_list) == 1:
            return self.add_owner_to_store_helper(new_owner_name, username, store_name,store)
        else:
            timeStamp = self.dateToStamp()
            message = "Hello, "+username+" want to add a new owner to the store, he is waiting for your approval..."
            waitingList = []  # {waitingName:'shaioz' ,[{owner:'yosi', approved: yes} ...]}
            store_from_domain = self.get_store_from_domain(store_name)
            for owner in owner_list:
                approved = True if owner.username == username else False
                waitingList.append({'owner': owner.username, 'approved': approved})
                self.send_notification_to_user(username, owner.username, timeStamp, message,'1')
            store_from_domain.waitingForBecomeOwner.append({'waitingName': new_owner_name, 'waitingList': waitingList})
            #self.database.add_store_owner(store_name, new_owner_name, username)
            return ResponseObject(True, False, "Waiting for the approval of the other owners")

    def add_item_to_inventory(self, username, store_name, item, quantity):
        store_result = self.get_store(store_name)
        if store_result is None:
            return ResponseObject(False, False,
                                  "Error: can't add items to store ")
        store = store_result.value
        find_user = self.get_user_or_guest(username)
        if find_user is None:
            return find_user
        curr_user = find_user.value
        add = store.add_item_to_inventory(curr_user, item, quantity)
        if not add.success:
            return ResponseObject(False, False, "Error: can't add " + item['name'] + " to" + store_name + "store\n"
                                  + add.message)
        self.database.add_item(item['name'], store_name, item['price'], item['category'], quantity, 0)
        self.log.set_info("adding item" + item['name'] + "to" + store_name + "succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def edit_item_price(self, username, store_name, itemname, new_price):
        store_result = self.get_store(store_name)
        if store_result is None:
            return ResponseObject(False, False,
                                  "Error: can't add items to store ")
        store = store_result.value
        find_user = self.get_user_or_guest(username)
        if find_user is None:
            return find_user
        curr_user = find_user.value
        item = store.search_item_by_name(itemname)
        if not item:
            return ResponseObject(False, False,
                                  "Error: no such product in " + store_name)
        if new_price > 0:
            add = store.edit_item_price(curr_user, itemname, new_price)
            if not add.success:
                return ResponseObject(False, False, "Error: can't edit " + itemname[
                    'name'] + "'s price in" + store_name + "store\n" + add.message)
            self.database.edit_item_price_in_db(store_name, itemname, new_price)
            return ResponseObject(True, True, "")

    def edit_item_quantity(self, username, store_name, itemname, quantity):
        store_result = self.get_store(store_name)
        if store_result is None:
            return ResponseObject(False, False,
                                  "Error: can't add items to store " + store_name)
        store = store_result.value
        find_user = self.get_user_or_guest(username)
        if find_user is None:
            return find_user
        curr_user = find_user.value
        item = store.get_item_quantity(itemname)
        if not item:
            return ResponseObject(False, False,
                                  "Error: no such product in " + store_name)
        add = store.edit_item_quantity(curr_user, {'name': itemname, 'quantity': item}, quantity)
        if add is None:
            return ResponseObject(False, False, "Error: can't add item " + itemname + " to store " + store_name + "\n" + add.message)
        self.database.edit_item_quantity_in_db(store_name, itemname, quantity)
        return ResponseObject(True, True, "")

    def approveNewOwner(self, new_owner_name, username, store_name):
        store = self.get_store_from_domain(store_name)
        allGivedApproved = True
        for user in store.waitingForBecomeOwner:
            if user['waitingName'] == new_owner_name:
                for owner in user['waitingList']:
                    if owner['owner'] == username:
                        owner['approved'] = True
                    allGivedApproved = allGivedApproved and owner['approved']
        if allGivedApproved :
            return self.add_owner_to_store_helper
        else:
            return ResponseObject(False, True, "")

    def add_owner_to_store_helper(self,new_owner_name,username,store_name,store):
        #store_result = self.get_store(store_name)
        #if not store_result.success:
        #    return store_result
        #store = store_result.value
        new_owner_obj = self.get_user(new_owner_name)
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        add = self.add_new_owner(curr_user, new_owner_obj,store)
        if not add.success:
            return add
        self.log.set_info("adding owner succeeded", "eventLog")
        return ResponseObject(True, True, "")

    # 4.3
    # owner, new_owner = User(...)
    def add_new_owner(self, owner_obj, new_owner_obj, store_obj):
        if isinstance(owner_obj, User) and owner_obj.logged_in:
            if store_obj.check_if_store_owner(owner_obj):
                if not store_obj.check_if_store_owner(new_owner_obj):
                    self.database.add_store_owner(store_obj.name, new_owner_obj.username, owner_obj.username)
                    #store_obj.storeOwners.append(
                    #    StoreOwner(new_owner_obj.username, new_owner_obj.password, new_owner_obj.age, new_owner_obj.country, owner_obj))
                    #for k in store_obj.storeOwners:
                    #    if k.username == owner_obj.username:
                    #        k.add_appointee(new_owner_obj)
                    store_obj.log.set_info("new store owner has been added successfully!", "eventLog")
                    return ResponseObject(True, True, "")
                else:
                    store_obj.log.set_info("error: user is already an owner of this store", "eventLog")
                    return ResponseObject(False, False,
                                          "User" + new_owner_obj.username + " is already an owner of this store")
            else:
                store_obj.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User " + owner_obj.username + " is not an owner of this store")
        else:
            store_obj.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    def remove_owner_from_store(self, store_name, owner_to_remove, username):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_owner_obj = self.get_user(owner_to_remove)
        if new_owner_obj is None:
            self.log.set_info("error: remove owner failed: user is not in the system", "eventLog")
            return ResponseObject(False, False, owner_to_remove + " is not a user in the system")
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        remove = store.remove_owner(curr_user, new_owner_obj)
        if not remove.success:
            return remove
        self.database.remove_store_owner(store_name, owner_to_remove)
        self.log.set_info("remove owner succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def add_manager_to_store(self, store_name, new_manager_name, permissions, username):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_manager_obj = self.get_user(new_manager_name)
        if new_manager_obj is None:
            self.log.set_info("error: adding manager failed: user is not in the system", "eventLog")
            return ResponseObject(False, False, new_manager_name + " is not a user in the system")
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        add = store.add_new_manager(curr_user, new_manager_obj, permissions)
        if not add.success:
            return add
        self.database.add_store_manager(store_name, new_manager_name, username, 0, 0, 0, 0)
        self.log.set_info("adding manager succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def remove_manager_from_store(self, store_name, manager_to_remove, username):
        store_result = self.get_store(store_name)
        if not store_result.success:
            return store_result
        store = store_result.value
        new_manager_obj = self.get_user(manager_to_remove)
        if new_manager_obj is None:
            self.log.set_info("error: removing manager failed: user is not in the system", "eventLog")
            return ResponseObject(False, False, manager_to_remove + " is not a user in the system")
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        remove = store.remove_manager(curr_user, new_manager_obj)
        if not remove.success:
            return remove
        self.log.set_info("removing manager succeeded", "eventLog")
        self.database.remove_store_manager(manager_to_remove, store_name)
        return ResponseObject(True, True, "")

    # helper function for buy_items
    def get_total_amount(self, items):
        total_price = 0
        for item in items:
            store = self.get_store(item['store_name'])
            item_obj = store.search_item_by_name(item['name'])
            if not item_obj:
                return False
            total_price += item_obj.apply_discount()
        return total_price

    def get_supply(self, supply_details):
        if not self.supplying_system.supply_handshake():
            return False
        transaction = self.supplying_system.supply(supply_details['name'], supply_details['address'],
                                                   supply_details['city'], supply_details['country'],
                                                   supply_details['zip'])
        if transaction < 0:
            return False
        return transaction

    def pay(self, collect_details):
        if not self.collecting_system.collect_handshake():
            return False
        transaction = self.collecting_system.pay(collect_details['card_number'], collect_details['month'],
                                                 collect_details['year'], collect_details['holder'],
                                                 collect_details['ccv'], collect_details['policyid'])
        if transaction < 0:
            return False
        return transaction

    def buy_items(self, items, username, supply_details, collect_details):
        # check if items exist in basket??
        for item in items:
            store = self.get_store(item['store_name'])
            if not store.success:
                self.log.set_info("error: buy items failed: store does not exist", "eventLog")
                return ResponseObject(False, False, "buy items failed: Store " + item['store_name'] + " does not exist")
        # get current user
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        amount = self.get_total_amount(items)
        if not amount:
            return ResponseObject(False, False, "Buy items failed: one of the items doesn't exist in the system")
        # get supply
        supply_id = self.get_supply(supply_details)
        if not supply_id:
            return ResponseObject(False, False, "Buy items failed: can't get supply for user " + username)
        # payment
        pay_id = self.pay(collect_details)
        if not pay_id:
            return ResponseObject(False, False, "Buy items failed: Payment Rejected")
        # remove items from user's basket
        for item in items:
            removed = curr_user.remove_from_cart(item['store_name'], item['name'])
            if not removed.success:
                self.supplying_system.cancel_supply(supply_id)
                self.collecting_system.cancel_pay(pay_id)
                self.log.set_info("error: buy items failed", "eventLog")
                return ResponseObject(False, False, "Cannot purchase item " + item.name + "\n" + removed.message)
            store = self.get_store(item['store_name'])
            quantity_to_remove = self.database.get_quantity_from_cart((item.name, store))
            quantity_to_remove *= -1
            self.database.edit_item_quantity_in_db(store, item.name, quantity_to_remove)
        if isinstance(curr_user, User):
            self.database.remove_basket(username)
        self.log.set_info("buy items succeeded", "eventLog")
        return ResponseObject(True, amount, "")

    def create_store(self, store_name, username):
        if username not in self.loggedInUsers:
            self.log.set_info("error: create store failed: user is not a subscriber in the system", "eventLog")
            return ResponseObject(False, None, "User " + username +
                                  " is not a subsciber in the system, or is not logged in")
        b = False
        for stur in self.stores:
            if stur.name == store_name:
                b = True
        if b:
            self.log.set_info("error: create store failed: store already exists", "eventLog")
            return ResponseObject(False, None, "Store already exists")
        else:
            new_store = Store(store_name, self.loggedInUsers[username])
            self.database.add_store(new_store, username)
            self.stores.append(new_store)
            self.log.set_info("create store succeeded", "eventLog")
            return ResponseObject(True, new_store, "")

    def remove_user(self, user_to_remove, username):
        if username not in self.loggedInUsers:
            self.log.set_info("error: remove user failed: user is not a subscriber in the system", "eventLog")
            return ResponseObject(False, None, "User " + username +
                                  " is not a subsciber in the system, or is not logged in")
        if username != self.system_manager.username:
            self.log.set_info("error: removing user failed: user is not a system manager", "eventLog")
            return ResponseObject(False, False, "You can't remove a user, you are not the system manager")
        if self.system_manager.username == user_to_remove:
            self.log.set_info("error: removing user failed: user can't remove himself", "eventLog")
            return ResponseObject(False, False, "You can't remove yourself silly")
        if not self.does_user_exist_in_db(user_to_remove):
            self.log.set_info("error: removing user failed: " + user_to_remove + " is not a user", "eventLog")
            return ResponseObject(False, False, user_to_remove + " is not a user")
        stores_to_remove = []
        for store in self.stores:
            if len(store.storeOwners) == 1 and user_to_remove == store.storeOwners[0].username:
                stores_to_remove.append(store)
        for st in stores_to_remove:
            self.stores.remove(st)
        self.loggedInUsers.pop(user_to_remove)
        # self.users.pop(user_to_remove)
        self.database.remove_user(user_to_remove)
        self.log.set_info("removing user succeeded", "eventLog")
        return ResponseObject(True, True, "User " + user_to_remove + " removed")

    def get_store(self, store_name):

        store_from_db = self.database.get_store(store_name)
        resp = ResponseObject(False, None, "no such store") if store_from_db is None else ResponseObject(True, store_from_db, "")
        return resp
        # for stor in self.stores:
        #     if store_name == stor.name:
        #         self.log.set_info("get store succeeded", "eventLog")
        #         # store_from_db = self.database.get_store(store_name)
        #         return ResponseObject(True, stor, "")
        # self.log.set_info("error: get store failed: store doesn't exist in the system", "eventLog")
        # return ResponseObject(False, None, "Store " + store_name + " doesn't exist in the system")

    def get_basket(self, username):
        # TODO: basket from db !
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        non_empty = 0
        basket_ret = []
        basket = curr_user.get_basket()
        for cart in basket.carts:
            if len(cart.items_and_quantities) > 0:
                non_empty = 1
            cart_ret = []
            store = self.get_store(cart.store_name).value
            for product in cart.items_and_quantities:
                item = store.get_item_if_available(product, cart.items_and_quantities.get(product))
                quantity = cart.items_and_quantities[product]
                cart_ret.append({'name': item.name, 'price': item.price, 'quantity': quantity,
                                'category': item.category, 'rank': item.rank, 'discount': ''})
            basket_ret.append({'cart': cart_ret, 'store': store.name})
        return ResponseObject(False, False, "") if non_empty == 0 else ResponseObject(True, basket_ret, "")

    def get_basket_size(self, username):
        basket = self.get_basket(username)
        size = 0
        if basket.success:
            for cart in basket.value:
                for item in cart['cart']:
                    size += 1
        return ResponseObject(True, size, "")

    def get_user(self, username):
        return self.database.get_user(username)
        # if username in self.users:
        # print(self.users[username])
        # return self.users[username]
        # return None

    def does_user_exist_in_db(self, username):
        return self.database.does_user_exist(username)

    def add_to_cart(self, store_name, item_name, quantity, username):
        result = self.get_store(store_name)
        if not result.success:
            self.log.set_info("error: adding to cart failed: no such store", "eventLog")
            return ResponseObject(False, False, result.message)
        store = result.value
        available = store.get_item_if_available(item_name, quantity)
        if not available:
            self.log.set_info("error: adding to cart failed: item is not available", "eventLog")
            return ResponseObject(False, False, "Item " + item_name + "is not available")
        find_user = self.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        item = store.search_item_by_name(item_name)
        old_cart = curr_user.get_cart(store_name)
        tmp_cart = old_cart.value.copy_cart()
        tmp_cart.add_item_to_cart(item_name, quantity)
        if not store.buying_policy.apply_policy(tmp_cart):
            self.log.set_info("error: adding to cart failed: store policy", "eventLog")
            return ResponseObject(False, False, "Store policy")
        if not item.buying_policy.apply_policy(tmp_cart):
            self.log.set_info("error: adding to cart failed: store policy", "eventLog")
            return ResponseObject(False, False, "Store policy")
        curr_user.add_to_cart(store_name, item_name, quantity)
        self.database.add_cart(username, store_name, item_name, quantity)
        self.log.set_info("adding to cart succeeded", "eventLog")
        return ResponseObject(True, True, "")

    def get_total_system_inventory(self):

        retList = []
        prods = self.database.get_all_products()
        for item in prods:
            new_item = {'name': item['name'], 'category': item['val'].category, 'price': item['val'].price,
                        'quantity': item['quantity'], 'store': item['val'].store_name}
            retList.append(new_item)
        return ResponseObject(True, retList, "")

    def get_store_inventory_from_db(self, store_name):
        return self.database.get_store_inventory_from_db(store_name)

    def get_user_type(self, username):
        if username == self.system_manager.username:
            return "sys_manager"
        return self.database.get_user_type(username)


    def get_stores(self):
        stores = self.database.get_all_stores()
        return stores

    def send_notification_to_user(self, sender_username, receiver_username, key, message, typ):
        self.database.add_notification(sender_username, receiver_username, key, message, typ)

    def get_user_notifications_from_db(self, user_name):
        res = self.database.get_user_notification(user_name)
        return ResponseObject(True, res, '')
        # response = {True, ret_list, ''}
        # return response

    def remove_user_notifications_from_db(self, user_name):
        self.database.remove_user_notifications(user_name)
        return ResponseObject(True, True, '')

    def add_item_policy(self, item_name, store_name, policy, user_name):

        parsed_policy = self.parse_item_policy(policy, item_name)
        store_ans = self.get_store(store_name)
        if not store_ans.success:
            self.log.set_info("error: adding policy failed: store doesnt exist", "eventLog")
            return ResponseObject(False, False, "Store doesnt exist")
        store = store_ans.value
        if not store.check_if_store_owner(self.get_user(user_name)):
            self.log.set_info("error: adding policy failed: not an store owner", "eventLog")
            return ResponseObject(False, False, "Store permission denied")
        item = store.search_item_by_name(item_name)
        if policy['override'] == 'True':
            item.set_buying_policy(parsed_policy)
        else:
            item.add_buying_policy(parsed_policy, (policy['combo'] == 'True'))
        self.database.add_item_policy(item_name, store_name, policy['type'], policy['combo'],
                                      policy['args'], policy['override'])
        return ResponseObject(True, True, "")

    def add_store_policy(self, store_name, policy, user_name):

        parsed_policy = self.parse_store_policy(policy, store_name)
        store_ans = self.get_store(store_name)
        if not store_ans.success:
            self.log.set_info("error: adding policy failed: store doesnt exist", "eventLog")
            return ResponseObject(False, False, "Store doesnt exist")
        store = store_ans.value
        if not store.check_if_store_owner(self.get_user(user_name)):
            self.log.set_info("error: adding policy failed: not an store owner", "eventLog")
            return ResponseObject(False, False, "Store permission denied")
        if policy['override'] == 'True':
            store_name.set_buying_policy(parsed_policy)
        else:
            store_name.add_buying_policy(parsed_policy, (policy['combo'] == 'True'))
        self.database.add_policy_to_store(store_name, policy['type'], policy['combo'],
                                          policy['args'], policy['override'])
        return ResponseObject(True, True, "")

    @staticmethod
    def parse_item_policy(policy, item_name):
        new_policy = None
        if policy['type'] == 'age':
            new_policy = AgeLimitationUserPolicy(policy['args'])
        elif policy['type'] == 'country':
            new_policy = CountryLimitationUserPolicy(policy['args'])
        elif policy['type'] == 'min':
            new_policy = MinQuantityItemPolicy(item_name, policy['args'])
        elif policy['type'] == 'max':
            new_policy = MaxQuantityItemPolicy(item_name, policy['args'])
        return new_policy

    @staticmethod
    def parse_store_policy(policy, store_name):
        new_policy = None
        if policy['type'] == 'min':
            new_policy = MinQuantityStorePolicy(store_name, policy['args'])
        elif policy['type'] == 'max':
            new_policy = MaxQuantityStorePolicy(store_name, policy['args'])
        return new_policy

    def get_store_from_domain(self, store_name):
        for store in self.stores:
            if store.name == store_name:
                return store;

    def dateToStamp(self):
        now = datetime.now()
        return datetime.timestamp(now)
