from .StoreOwner import StoreOwner
from .DiscountPolicy import DiscountPolicy
from .ProcurementPolicy import ProcurementPolicy
from .User import User
from .StoreManager import StoreManager


# Interface
class Store(object):

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.inventory = {}
        self.storeOwners = []
        self.storeManagers = []
        self.discountPolicy = 0
        self.procPolicy = 0

    def set_proc_policy(self, new_policy):
        if isinstance(new_policy, ProcurementPolicy):
            self.procPolicy = new_policy
            print("new policy has updated")
            return True
        print("illegal policy")
        return False

    def check_if_store_owner(self, user):
        if isinstance(user, User):
            for k in self.storeOwners:
                if k.username == user.username:
                    return True
        return False

    def check_if_store_manager(self, user):
        if isinstance(user, User):
            for k in self.storeManagers:
                if k.username == user.username:
                    return True
        return False

    # 4.1.1
    def add_item_to_inventory(self, user, item, quantity):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                if item in self.inventory:
                    self.inventory[item] += quantity
                else:
                    self.inventory[item] = quantity
                print("item has been successfully added to the store inventory!")
                return True
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    # 4.1.2
    def remove_item_by_quantity(self, user, item, quantity):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                if item in self.inventory:
                    if self.inventory[item] >= quantity:
                        self.inventory[item] -= quantity
                        print("items has been successfully removed from the store inventory!")
                        return True
                    else:
                        print("not enough items for this quantity")
                        return False
                else:
                    print("item is not in the inventory of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    def remove_item_from_inventory(self, user, item):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                if item in self.inventory:
                    del self.inventory[item]
                    print("item has been successfully removed from the store inventory!")
                    return True
                else:
                    print("item is not in the inventory of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    # 4.1.3
    # user field added
    def edit_item_price(self, user, item, new_price):
        if isinstance(user, StoreOwner) and user.logged_in:
            if user in self.storeOwners:
                if item in self.inventory:
                    for k in self.inventory.keys():
                        if item.name == k.name:
                            k.set_price(new_price)
                            print("item's price has been successfully updated!!")
                            return True
                else:
                    print("item is not in the inventory of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    def set_discount_policy(self, new_policy):
        if isinstance(new_policy, DiscountPolicy):
            self.discountPolicy = new_policy
            print("new discount policy has updated")
            return True
        else:
            print("illegal discount policy")
            return False

    # 4.3
    def add_new_owner(self, owner, new_owner):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if not self.check_if_store_owner(new_owner):
                    self.storeOwners.append(StoreOwner(new_owner.username, new_owner.password, owner))
                    for k in self.storeOwners:
                        if k.username == owner.username:
                            k.add_appointee(new_owner)
                    print("new store owner has been added successfully!")
                    return True
                else:
                    print("user is already an owner of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    # 4.4
    def remove_owner(self, owner, owner_to_remove):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if self.check_if_store_owner(owner_to_remove):
                    for k in self.storeOwners:
                        if k.username == owner.username:
                            if k.is_appointee(owner_to_remove):
                                for x in self.storeOwners:
                                    if x.username == owner_to_remove.username:
                                        for i in x.get_appointees():
                                            self.remove_owner(owner_to_remove, i)
                                    self.storeOwners.remove(x)
                                    k.remove_appointee(owner_to_remove)
                                    print("store owner has been removed successfully!")
                                    return True
                                for x in self.storeManagers:
                                    if x.username == owner_to_remove:
                                        self.storeManagers.remove(x)
                                        k.remove_appointee(owner_to_remove)
                                        print("store manager has been removed successfully!")
                                        return True
                            print("the owner is not the appointer for this owner")
                            return False
                else:
                    print("user is not an owner of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    # 4.5
    def add_new_manager(self, owner, new_manager, permissions):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if not self.check_if_store_manager(new_manager):
                    self.storeManagers.append(StoreManager(new_manager.username, new_manager.password, owner, permissions))
                    for k in self.storeManagers:
                        if k.username == owner.username:
                            k.add_appointee(new_manager)
                    print("new store manager has been added successfully!")
                    return True
                else:
                    print("user is already a manager of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return True

    def set_permissions_to_manager(self, owner, manager, permissions):
        for k in self.storeOwners:
            if k.username == owner.username:
                if k.is_appointee(manager):
                    for x in self.storeManagers:
                        if x.username == manager.username:
                            x.set_permissions(permissions)
                            print("permissions for manager has updated")
                            return True
                print("owner is not the manager appointer")
                return False
            print("user is not a store owner")
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
                                    if x.username == manager_to_remove:
                                        self.storeManagers.remove(x)
                                        k.remove_appointee(manager_to_remove)
                                        print("store manager has been removed successfully!")
                                        return True
                            print("the owner is not the appointer for this manager")
                            return False
                else:
                    print("user is not a manager of this store")
                    return False
            else:
                print("user is no store manager for this store")
                return False
        else:
            print("user is not logged in or not a store manager")
            return True

    def search_item_by_name(self, item_name):
        result_list = []
        for item in self.inventory.keys():
            if item.name == item_name:
                result_list += item
        return result_list

    def search_item_by_price(self, price):
        result_list = []
        for item in self.inventory.keys():
            if item.price == price:
                result_list += item
        return result_list

    def search_item_by_category(self, category):
        result_list = []
        for item in self.inventory.keys():
            if item.category == category:
                result_list += item
        return result_list
