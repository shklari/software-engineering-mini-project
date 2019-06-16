from Domain.StoreOwner import StoreOwner
from Domain.DiscountPolicy import DiscountPolicy
from Domain.User import User
from Domain.StoreManager import StoreManager
from Domain.Item import Item
from log.Log import Log
from Domain.Response import ResponseObject
from Domain.Discounts.ComposedDiscount import *
from Domain.BuyingPolicy import *


# Interface
class Store(object):

    def __init__(self, name, owner):
        self.name = name
        self.rank = 0
        self.inventory = []
        self.storeOwners = [StoreOwner(owner.username, owner.password, owner.age, owner.country)]
        self.storeManagers = []
        self.waitingForBecomeOwner =[] # {waitingName:'shaioz' ,[{owner:'yosi', approved: yes} ...]}
        self.discountPolicy = 0
        self.log = Log("", "")
        self.discount = ComposedDiscount(0, 0, True, "")
        self.buying_policy = ImmediateBuyingPolicy()
        # self.errorLog = ErrorLog()

    def check_if_store_owner(self, user):
        if isinstance(user, User):  # fixxxxx (check instance of store owner)
            for k in self.storeOwners:
                if k.username == user.username:
                    return True
        return False

    def check_if_store_manager(self, user):
        if isinstance(user, User):  # fixxxx (check instance of store manager)
            for k in self.storeManagers:
                if k.username == user.username:
                    return True
        return False

    # 4.1.1 - added new product to inventory
    # item = {'name': str, 'price': int, 'category': str}
    def add_item_to_inventory(self, user, item, quantity):
        if quantity >= 0:
            if isinstance(user, User) and user.logged_in:
                if self.check_if_store_owner(user):
                    if len(self.inventory) == 0:
                        self.inventory = [{'name': item['name'],
                                           'val': Item(item['name'], item['price'], item['category'], self.name),
                                           'quantity': quantity}]
                        self.log.set_info('item has been successfully added to the store inventory!', 'eventLog')
                        return ResponseObject(True, True, "")
                    else:
                        self.inventory.append({'name': item['name'],
                                           'val': Item(item['name'], item['price'], item['category'], self.name),
                                           'quantity': quantity})
                        self.log.set_info('item has been successfully added to the store inventory!', 'eventLog')
                        return ResponseObject(True, True, "")
                        # flag = False
                        # for x in self.inventory:
                        #     if x['val'].name == item['name']:
                        #         flag = True
                        # if not flag:
                        #     self.inventory = [{'name': item['name'],
                        #                        'val': Item(item['name'], item['price'], item['category'], self.name),
                        #                        'quantity': quantity}]
                        #     self.log.set_info('item has been successfully added to the store inventory!', 'eventLog')
                        #     return ResponseObject(True, True, "")
                        # return ResponseObject(False, False, "item already exist")
                else:
                    self.log.set_info('error: user is no store owner for this store', 'eventLog')
                    return ResponseObject(False, False, "User is not an owner of store " + self.name)
            else:
                self.log.set_info('error: user is not logged in or not a store owner', 'eventLog')
                return ResponseObject(False, False, "User is not logged in or is not a store owner")
        else:
            self.log.set_info('error: invalid quantity', 'eventLog')
            return ResponseObject(False, False, "Invalid quantity")

    # add quantity to specific item
    def edit_item_quantity(self, user, item, quantity):
        if quantity >= 0:
            if isinstance(user, User) and user.logged_in:
                if self.check_if_store_owner(user):
                    if len(self.inventory) == 0:
                        return ResponseObject(False, False, "no such item in inventory")
                    else:
                        flag = False
                        for x in self.inventory:
                            if x['val'].name == item['name']:
                                x['quantity'] += quantity
                                flag = True
                                break
                        if not flag:
                            return ResponseObject(False, False, "no such item in inventory")
                        self.log.set_info('item/''s quantity has been successfully edited!', 'eventLog')
                        return ResponseObject(True, True, "")
                else:
                    self.log.set_info('error: user is no store owner for this store', 'eventLog')
                    return ResponseObject(False, False, "User is not an owner of store " + self.name)
            else:
                self.log.set_info('error: user is not logged in or not a store owner', 'eventLog')
                return ResponseObject(False, False, "User is not logged in or is not a store owner")
        else:
            self.log.set_info('error: invalid quantity', 'eventLog')
            return ResponseObject(False, False, "Invalid quantity")

    # 4.1.2
    def remove_item_by_quantity(self, user, itemname, quantity):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        if x['quantity'] >= quantity:
                            x['quantity'] -= quantity
                            self.log.set_info("items has been successfully removed from the store inventory!",
                                              "eventLog")
                            return ResponseObject(True, True, "")
                        else:
                            self.log.set_info("error: not enough items for this quantity", "eventLog")
                            return ResponseObject(False, False, "Item " + itemname + " doesn't exist in this quantity")
                    else:
                        self.log.set_info("error: item is not in the inventory of this store", "eventLog")
                        return ResponseObject(False, False, "Item doesn't exist in this store's inventory")
            else:
                self.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User is not an owner of store " + self.name)
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not a store owner")

    def remove_item_from_inventory(self, user, itemname):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        self.inventory.remove(x)
                        self.log.set_info("item has been successfully removed from the store inventory!", "eventLog")
                        return ResponseObject(True, True, "")

                self.log.set_info("error: item is not in the inventory of this store", "eventLog")
                return ResponseObject(False, False, "Item " + itemname + " doesn't exist in the inventory of " + self.name)
            else:
                self.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User is not an owner of store " + self.name)
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    # 4.1.3
    def edit_item_price(self, user, itemname, new_price):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        x['val'].set_price(new_price)
                        self.log.set_info("item's price has been successfully updated", "eventLog")
                        return ResponseObject(True, True, "")

                self.log.set_info("error: item is not in the inventory of this store", "eventLog")
                return ResponseObject(False, False, "Item " + itemname + " doesn't exist in" + self.name + "'s inventory")

            else:
                self.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User is not an owner of store " + self.name)
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    def set_discount_policy(self, new_policy):
        if isinstance(new_policy, DiscountPolicy):
            self.discountPolicy = new_policy
            self.log.set_info("new discount policy has updated", "eventLog")
            return True
        else:
            self.log.set_info("error: illegal discount policy", "eventLog")
            return False

    # 4.3
    # owner, new_owner = User(...)
    def add_new_owner(self, owner, new_owner):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if not self.check_if_store_owner(new_owner):
                    self.storeOwners.append(StoreOwner(new_owner.username, new_owner.password, new_owner.age, new_owner.country, owner))
                    for k in self.storeOwners:
                        if k.username == owner.username:
                            k.add_appointee(new_owner)
                    self.log.set_info("new store owner has been added successfully!", "eventLog")
                    return ResponseObject(True, True, "")
                else:
                    self.log.set_info("error: user is already an owner of this store", "eventLog")
                    return ResponseObject(False, False, "User" + new_owner.username + " is already an owner of this store")
            else:
                self.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User " + owner.username + " is not an owner of this store")
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    # 4.4
    # owner, owner_to_remove = User(...)
    def remove_owner(self, owner, owner_to_remove):
        owner_type = 0
        for k in self.storeOwners:
            if k.username == owner.username:
                owner_type = k
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if self.check_if_store_owner(owner_to_remove):
                    if owner_type.is_appointee(owner_to_remove):
                        to_remove = self.remove_owner_rec(owner, owner_to_remove)
                    else:
                        self.log.set_info("error: user is not the appointer", "eventLog")
                        return ResponseObject(False, False, "User " + owner.username + " is not the appointer of user " + owner_to_remove.username)
                else:
                    self.log.set_info("error: user is not an owner of this store", "eventLog")
                    return ResponseObject(False, False, "User " + owner_to_remove.username + " is not an owner of this store")
            else:
                self.log.set_info("error: user is not an owner of this store", "eventLog")
                return ResponseObject(False, False, "User " + owner.username + " is not an owner of this store")
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

        for x in to_remove:
            for y in self.storeOwners:
                if x.username == y.username:
                    self.storeOwners.remove(y)
            for z in self.storeManagers:
                if x.username == z.username:
                    self.storeManagers.remove(z)
        for x in owner_type.appointees:
            if x.username == owner_to_remove.username:
                owner_type.appointees.remove(x)
        self.log.set_info("owner has been successfully removed", "eventLog")
        return ResponseObject(True, True, "")

    def remove_owner_rec(self, owner, owner_to_remove):
        to_remove = []
        owner_type = 0
        owner_to_remove_type = 0
        for k in self.storeOwners:
            if k.username == owner.username:
                owner_type = k
            if k.username == owner_to_remove.username and owner.username != owner_to_remove.username:
                owner_to_remove_type = k

        if owner_type != 0 and owner_to_remove_type == 0:
            return to_remove

        for tmp in owner_to_remove_type.appointees:
            to_remove.append(self.remove_owner_rec(owner_to_remove, tmp))
        to_remove.append(owner_to_remove)
        return to_remove

    # 4.5
    # permissions = {'Edit': Boolean, 'Remove': Boolean, 'Add': Boolean, 'Discounts': Boolean}
    def add_new_manager(self, owner, new_manager, permissions):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if not self.check_if_store_manager(new_manager):
                    self.storeManagers.append(
                        StoreManager(new_manager.username, new_manager.password, new_manager.age, new_manager.country, owner, permissions))
                    for k in self.storeOwners:
                        if k.username == owner.username:
                            k.add_appointee(new_manager)
                    self.log.set_info("new store manager has been added successfully!", "eventLog")
                    return ResponseObject(True, True, "")
                else:
                    self.log.set_info("error: user is already a manager of this store", "eventLog")
                    return ResponseObject(False, False, "User " + new_manager.username + " is already a manager of this store")
            else:
                self.log.set_info("error: user is no store owner for this store", "eventLog")
                return ResponseObject(False, False, "User " + owner.username + " is not an owner of this store")
        else:
            self.log.set_info("error: user is not logged in or not a store owner", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    def set_permissions_to_manager(self, owner, manager, permissions):
        for k in self.storeOwners:
            if k.username == owner.username:
                if k.is_appointee(manager):
                    for x in self.storeManagers:
                        if x.username == manager.username:
                            x.set_permissions(permissions)
                            self.log.set_info("permissions for manager has updated", "eventLog")
                            return True
                self.log.set_info("error: owner is not the manager appointer", "eventLog")
                return False
            self.log.set_info("error: user is not a store owner", "eventLog")
            return False

    # 4.6
    def remove_manager(self, owner, manager_to_remove):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if self.check_if_store_manager(manager_to_remove):
                    for k in self.storeOwners:
                        if k.username == owner.username:
                            if k.is_appointee(manager_to_remove):
                                for x in self.storeManagers:
                                    if x.username == manager_to_remove.username:
                                        self.storeManagers.remove(x)
                                        k.remove_appointee(manager_to_remove)
                                        self.log.set_info("store manager has been removed successfully!", "eventLog")
                                        return ResponseObject(True, True, "")
                            self.log.set_info("error: the owner is not the appointer for this manager", "eventLog")
                            return ResponseObject(False, False, "The user " + owner.username + " is not the appointer of manager " + manager_to_remove.username)
                else:
                    self.log.set_info("error: user is not a manager of this store", "eventLog")
                    return ResponseObject(False, False, "User " + manager_to_remove.username + " is not a manager of this store")
            else:
                self.log.set_info("error: user is no store manager for this store", "eventLog")
                return ResponseObject(False, False, "User " + owner.username + " is not an owner of this store")
        else:
            self.log.set_info("error: user is not logged in or not a store manager", "eventLog")
            return ResponseObject(False, False, "User is not logged in or is not an owner of the store")

    def search_item_by_name(self, item_name):
        for item in self.inventory:
            if item['name'] == item_name:
                print(item['val'])
                return item['val']
        return False

    def search_item_by_price(self, price):
        result_list = []
        for item in self.inventory:
            if item['val'].price == price:
                result_list.append(item['val'])
        return result_list

    def search_item_by_category(self, category):
        result_list = []
        for item in self.inventory:
            if item['val'].category == category:
                result_list.append(item['val'])
        return result_list

    def get_item_if_available(self, item_name, quantity):
        boo = False
        for k in self.inventory:
            if k['name'] == item_name:
                if k['quantity'] >= quantity:
                    boo = True
                    break
        return self.search_item_by_name(item_name) if boo else False

    # discount is a Discount object
    def add_store_discount(self, user, discount):
        if not isinstance(user, User):
            return ResponseObject(False, False, "The user is not recognized in the system")
        if not user.logged_in:
            return ResponseObject(False, False, "User " + user.username + " is not logged in")
        if self.check_if_store_owner(user) or (self.check_if_store_manager(user) and user.permissions['Discounts']):
            self.discount.add_discount(discount)
            self.set_double_discount(self.discount.double & discount.double)
            return ResponseObject(True, self.discount, "")
        else:
            return ResponseObject(False, False,
                                  "User " + user.username +
                                  " is not a store owner or a store manager with the right permissions")

    def add_discount_to_item(self, user, item_name, discount):
        if not isinstance(user, User):
            return ResponseObject(False, False, "The user is not recognized in the system")
        if not user.logged_in:
            return ResponseObject(False, False, "User " + user.username + " is not logged in")
        item = self.search_item_by_name(item_name)
        if not item:
            return ResponseObject(False, False, "Item " + item_name + " doesn't exist in this store's inventory")
        elif self.check_if_store_owner(user) or (self.check_if_store_manager(user) and user.permissions['Discounts']):
            item.add_discount(discount)
            return ResponseObject(True, item, "")
        else:
            return ResponseObject(False, False,
                                  "User " + user.username +
                                  " is not a store owner or a store manager with the right permissions")

    def set_double_discount(self, double):
        self.discount.double = double

    def apply_store_discount(self, price):
        return self.discount.apply_discount(price)

    def apply_discounts(self, item_name):
        item = self.search_item_by_name(item_name)
        if not item:
            return ResponseObject(False, False, "Item " + item_name + " doesn't exist in store " + self.name)
        else:
            new_price = item.apply_discount()
            if self.discount.double:
                new_price = self.apply_store_discount(new_price)
            return ResponseObject(True, new_price, "")

    def set_buying_policy(self, policy):
        # check = self.check_access(user, 'Policy')
        # if not check.success:
        #     return check.success
        self.buying_policy = policy
        return ResponseObject(True, self.buying_policy, "")

    def add_buying_policy(self, policy, combination):
        comp = None
        if not combination:
            comp = OrCompositeBuyingPolicy()
            comp.add_policy(policy)
            comp.add_policy(self.buying_policy)
        else:
            comp = AndCompositeBuyingPolicy()
            comp.add_policy(policy)
            comp.add_policy(self.buying_policy)
        self.buying_policy = comp
        return ResponseObject(True, comp, "")

    def remove_buying_policy(self, policy):
        if self.buying_policy == policy:
            self.buying_policy = ImmediateBuyingPolicy()
        elif self.buying_policy.is_composite():
            self.buying_policy.remove_policy(policy)

    def check_access(self, user, query):
        if not isinstance(user, User):
            return ResponseObject(False, False, "The user is not recognized in the system")
        if not user.logged_in:
            return ResponseObject(False, False, "User " + user.username + " is not logged in")
        if self.check_if_store_owner(user) or (self.check_if_store_manager(user) and user.permissions[query]):
            return ResponseObject(True, True, "User " + user.username + " is not logged in")
        return ResponseObject(False, False, "User " + user.username + " has no permission")

    def get_inventory(self):
        ans = []
        for item in self.inventory:
            ans.append({'name': item['name'],
                        'category': item['val'].category,
                        'price': item['val'].price,
                        'quantity': item['quantity']})
        return ResponseObject(True, ans, '')



