from .StoreOwner import StoreOwner
from .DiscountPolicy import DiscountPolicy
from .ProcurementPolicy import ProcurementPolicy
from .User import User
from .StoreManager import StoreManager
from .Item import Item


# Interface
class Store(object):

    def __init__(self, name, owner):
        self.name = name
        self.rank = 0
        self.inventory = []
        self.storeOwners = [StoreOwner(owner.username, owner.password)]
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
    # item = {'name': str, 'price': int, 'category': str}
    def add_item_to_inventory(self, user, item, quantity):
        if quantity >= 1:
            if isinstance(user, User) and user.logged_in:
                if self.check_if_store_owner(user):
                    if len(self.inventory) == 0:
                        self.inventory = [{'name': item['name'], 'val': Item(item['name'], item['price'], item['category'], self.name), 'quantity': quantity}]
                        print("item has been successfully added to the store inventory!")
                        return True
                    else:
                        for x in self.inventory:
                            if x['val'].name == item['name']:
                                x['quantity'] += quantity
                            else:
                                self.inventory.append({'name': item['name'],
                                                       'val': Item(item['name'], item['price'], item['category'], self.name),
                                                       'quantity': quantity})
                            print("item has been successfully added to the store inventory!")
                            return True
                else:
                    print("user is no store owner for this store")
                    return False
            else:
                print("user is not logged in or not a store owner")
                return False
        else:
            print("invalid quantity")
            return False

    # 4.1.2
    def remove_item_by_quantity(self, user, itemname, quantity):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        if x['quantity'] >= quantity:
                            x['quantity'] -= quantity
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
            return False

    def remove_item_from_inventory(self, user, itemname):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        self.inventory.remove(x)
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
            return False

    # 4.1.3
    def edit_item_price(self, user, itemname, new_price):
        if isinstance(user, User) and user.logged_in:
            if self.check_if_store_owner(user):
                for x in self.inventory:
                    if x['name'] == itemname:
                        x['val'].set_price(new_price)
                        print("item's price has been successfully updated")
                        return True
                    else:
                        print("item is not in the inventory of this store")
                        return False
            else:
                print("user is no store owner for this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return False

    def set_discount_policy(self, new_policy):
        if isinstance(new_policy, DiscountPolicy):
            self.discountPolicy = new_policy
            print("new discount policy has updated")
            return True
        else:
            print("illegal discount policy")
            return False

    # 4.3
    # owner, new_owner = User(...)
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
            return False

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
                        print("user is not the appointer")
                        return False
                else:
                    print("user is not an owner of this store")
                    return False
            else:
                print("user is not an owner of this store")
                return False
        else:
            print("user is not logged in or not a store owner")
            return False

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
        print("owner has been successfully removed")
        return True

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
    # permissions = {'Edit': Boolean, 'Remove': Boolean, 'Add': Boolean}
    def add_new_manager(self, owner, new_manager, permissions):
        if isinstance(owner, User) and owner.logged_in:
            if self.check_if_store_owner(owner):
                if not self.check_if_store_manager(new_manager):
                    self.storeManagers.append(StoreManager(new_manager.username, new_manager.password, owner, permissions))
                    for k in self.storeOwners:
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
            return False

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
                                    if x.username == manager_to_remove.username:
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
            return False

    def search_item_by_name(self, item_name):
        for item in self.inventory:
            if item['name'] == item_name:
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
        return self.search_item_by_name(item_name) if boo else False
