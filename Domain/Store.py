from .StoreOwner import StoreOwner
from .DiscountPolicy import DiscountPolicy
from .ProcurementPolicy import ProcurementPolicy
from .User import User


# Interface
class Store(object):

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.inventory = dict.fromkeys(['item_name', 'quantity'])
        self.storeOwners = []
        self.storeManagers = []
        self.discountPolicy = 0
        self.procPolicy = 0

    def set_policy(self, new_policy):
        if isinstance(new_policy, ProcurementPolicy):
            self.procPolicy = new_policy;
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

    # 4.1.1
    def add_item_to_inventory(self, user, item, quantity):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                if item in self.inventory:
                    self.inventory[item] += quantity
                else:
                    self.inventory[item] = quantity
                print("item has been successesfuly added to the store inventory!")
                return True
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner at all")
            return True

    # 4.1.2
    def remove_item_from_inventory(self, user, item, quantity):
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
            print("user is not logged in or not a store owner at all")
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
            print("user is not logged in or not a store owner at all")
            return True

    def set_policy(self, new_policy):
        if isinstance(new_policy, DiscountPolicy):
            self.discountPolicy = new_policy
            print("new discount policy has updated")
            return True
        else:
            print("illegal discount policy")
            return False

    # 4.3
    def add_new_owner(self, owner, new_owner):
        if isinstance(owner, StoreOwner) and owner.logged_in:
            if owner in self.storeOwners:
                if new_owner not in self.storeOwners:
                    self.storeOwners.append(self, new_owner)
                    print("new store owner has been added successfully!")
                    return True
                else:
                    print("user is already an owner of this store")
                    return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner at all")
            return True

    # 4.4
    def remove_owner(self, owner, owner_to_remove): pass

    # 4.5
    def add_new_manager(self, owner, new_manager): pass

    # 4.6
    def remove_manager(self, owner, manager_to_remove): pass

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
