import pymongo
from django.utils.datetime_safe import datetime

from Domain.Item import Item
from Domain.Store import Store
from Domain.StoreOwner import StoreOwner
from Domain.User import User
from Domain.BuyingPolicy import *


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


class DB:
    def __init__(self):
        self.id = 1
        self.myclient = pymongo.MongoClient("mongodb+srv://grsharon:1234@cluster0-bkvsz.mongodb.net/test?retryWrites=true&w=majority")
        self.mydb = self.myclient["Store"]

    # adder functions

    def add_user(self, user):
        collection = self.mydb["Users"]
        user_to_add = {"name": user.username, "password": user.password, "age": user.age, "country": user.country}
        collection.insert_one(user_to_add)

    def add_store(self, store, username):
        collection = self.mydb["Stores"]
        store_to_add = {"name": store.name, "rank": store.rank}
        collection.insert_one(store_to_add)
        self.add_store_owner(store.name, username, 0)

    def add_store_owner(self, store_name, user_name, appointer):
        collection = self.mydb["StoreOwners"]
        store_owner_to_add = {"store_name": store_name, "owner": user_name, "appointer": appointer}
        collection.insert_one(store_owner_to_add)

    def add_store_manager(self, store_name, user_name, appointer, is_add_per, is_edit_per, is_remove_per, is_disc_per):
        collection = self.mydb["StoreManagers"]
        store_manager_to_add = {"store_name": store_name, "manager": user_name, "appointer": appointer,
                                "permission": {"add": is_add_per, "edit": is_edit_per,
                                               "remove": is_remove_per, "Discounts": is_disc_per}}
        collection.insert_one(store_manager_to_add)

    # policy = {type, combo, args, override}
    def add_item(self, item_name, store_name, price, category, quantity, policy):
        collection = self.mydb["Items"]
        item_to_add = {"name": item_name, "store": store_name, "price": price, "category": category,
                       "quantity": quantity, "policy": policy}
        # {"type": policy['type'], "combo": policy['combo'],
        #                                                 "args": policy['args'], "override": policy['override']}
        collection.insert_one(item_to_add)

    def add_item_policy(self, item_name, store_name, policy_type, policy_combo, policy_args, policy_ovveride):
        collection = self.mydb["Policies"]
        fatherson = self.mydb["PolicyComposed"]
        items = self.mydb['Items']
        if policy_ovveride == "true":
            self.remove_item_policy_by_name(item_name, store_name)
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.id}})
            collection.insert_one({"id": self.id, "type": policy_type, "combo": policy_combo, "args": policy_args})
            self.id += 1
        else:
            old_policyId = items.find_one({"name": item_name, "store": store_name})['policy']
            new_policy = {"id": self.id, "type": policy_type, "combo": policy_combo, "args": policy_args}
            comp_policy = {"id": self.id + 1, "type": "", "combo": policy_combo, "args": ""}
            collection.insert_many([new_policy, comp_policy])
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.id + 1}})
            fatherson.insert_many([{"father": self.id + 1, "son": old_policyId},
                                   {"father": self.id + 1, "son": self.id}])
            self.id += 2

    def add_notification(self, sender_username, receiver_username, key, message):
        collection = self.mydb["UserNotification"]
        not_to_add = {"sender_username": sender_username, "receiver_username": receiver_username,
                      "key": key, "message": message, "type": type}
        collection.insert_one(not_to_add)

    def add_cart(self, user_name, store_name, item_name, quantity):
        collection = self.mydb["Cart"]
        cart_to_add = {"user_name": user_name, "store_name": store_name, "item_name": item_name, "quantity": quantity}
        collection.insert_one(cart_to_add)

    def add_policy_to_item(self, store_name, item_name, new_policy): pass
    # TODO: set new policy to an item

    def add_policy_to_store(self, store_name, new_policy): pass
    # TODO: set new policy to a store

    # getters

    def get_user(self, user_name):
        if self.does_user_exist(user_name):
            curs = self.mydb.Users.find_one({"name": user_name})
            the_user = User(user_name, curs['password'], curs['age'], curs['country'])
            return the_user
        return None

    def does_user_exist(self, user_name):
        return True if self.mydb.Users.count_documents({"name": user_name}) > 0 else False

    def get_store(self, store_name):
        if self.does_store_exist(store_name):
            #owner_name = self.mydb.StoreOwners.find_one({"store_name": store_name}, {"owner": 1})
            #owner = self.get_user(owner_name)
            inventory = self.get_store_inventory_from_db(store_name)
            the_store = Store(store_name,'', inventory)
            return the_store
        return None

    def get_quantity_from_cart(self, item_name, store_name):
        return self.mydb.Cart.find_one({"item_name": item_name, "store_name": store_name})['quantity']

    def does_store_exist(self, store_name):
        return True if self.mydb.Stores.count_documents({"name": store_name}) > 0 else False

    def get_item_from_store(self, param, store_name):
        return self.mydb.Items.find({"store": store_name}, {"quantity": {"$gt": 0}},
                                    {"$or": [{"name": param}, {"price": param}, {"category": param}]})

    def get_store_inventory_from_db(self, store_name):
        if self.store_inventory_has_items(store_name):
            curs = self.mydb.Items.find({"store": store_name})
            ret_dict = []
            for item in curs:
                tmpobj = {"name": item['name'], "item": Item(item['name'], item['store'], item['price'],
                                                             item['category']), "quantity": item["quantity"]}
                # "policy": {"type": policy['type'], "combo": policy['combo'],
                #                                         "args": policy['args'], "override": policy['override']}
                ret_dict.append(tmpobj)
            return ret_dict
        return None
        # TODO: take policies from db and parse

    def store_inventory_has_items(self, store_name):
        return True if self.mydb.Items.count_documents({"store": store_name}) > 0 else False

    def get_user_type(self, user_name):
        if self.mydb.StoreOwners.count_documents({"owner": user_name}) > 0:
            return "store_owner"
        elif self.mydb.StoreManagers.count_documents({"manager": user_name}) > 0:
            return "store_manager"
        elif self.does_user_exist(user_name):
            return "user"
        return "guest"

    # return [{"message": , "sender": , "time": }]
    def get_user_notification(self, user_name):
        curs = self.mydb.UserNotification.find({"receiver_username": user_name})
        ret_list = []
        for notification in curs:
            time = self.stamp_to_date(notification['key'])
            msg = {"message": notification['message'], "sender": notification['sender_username'],
                   "time": '', "type": notification['type']}  # TODO: fix time to json serilize
            ret_list.append(msg)
        return ret_list

    def get_item_policy_by_id(self, policyId, item_name):
        sons = self.mydb.PolicyComposed.find({"father": policyId})
        policy = self.mydb.Policies.find_one({"id": policyId})
        if len(sons) == 0:
            return parse_item_policy(policy, item_name)
        comp_policy = AndCompositeBuyingPolicy() if policy['combo'] == "true" else OrCompositeBuyingPolicy()
        for iter in sons:
            sonId = iter['son']
            sonpolicy = self.get_item_policy_by_id(sonId, item_name)
            comp_policy.add_policy(sonpolicy)
        return comp_policy

    def get_store_owners_from_db(self, store_name):
        curs = self.mydb.StoreOwners.find({"store_name": store_name})
        ret_list = []
        for owner in curs:
            usr = self.get_user(owner['name'])
            owner_to_add = StoreOwner(usr.username, usr.password, usr.age, usr.country, owner['appointer'])
            ret_list.append(owner_to_add)
        return ret_list

    def get_item_policy_by_name(self, item_name, store_name):
        policyId = self.mydb.Items.find_one({"name": item_name, "store": store_name})['policy']
        if policyId == 0:
            return ItemPolicy()
        return self.get_item_policy_by_id(policyId, item_name)

    # return [{"message": , "sender": , "time": }]

    @staticmethod
    def stamp_to_date(stamp):
        return datetime.fromtimestamp(stamp)
    # editors

    def edit_item_price_in_db(self, store_name, item_name, new_price):
        collection = self.mydb["Items"]
        item_to_change = {"name": item_name, "store": store_name}
        collection.update_one(item_to_change, {"$set": {"price": new_price}})

    def edit_item_quantity_in_db(self, store_name, item_name, quantity):
            collection = self.mydb["Items"]
            item_to_change = {"name": item_name, "store": store_name}
            collection.update_one(item_to_change, {"$inc": {"quantity": quantity}})

    # removers

    def remove_user(self, user_name):
        collection = self.mydb["Users"]
        user_to_remove = {"name": user_name}
        collection.delete_one(user_to_remove)
        collection2 = self.mydb["StoreOwners"]
        owners_to_remove = {"appointer": user_name}
        collection2.delete_many(owners_to_remove)
        collection2.delete_many({"owner": user_name})
        collection3 = self.mydb["StoreManagers"]
        managers_to_remove = {"appointer": user_name}
        collection3.delete_many(managers_to_remove)
        collection3.delete_many({"manager": user_name})

    def remove_item_policy_by_id(self, id, item_name, store_name):
        fatherson = self.mydb.PolicyComposed
        if id > 0:
            sons = fatherson.find({"father": id})
            if sons.count() > 0:
                for son in sons:
                    sonId = son['son']
                    self.remove_item_policy_by_id(sonId)
                fatherson.delete_many({"father": id})
            self.mydb.Policies.delete_one({"id": id})
            self.mydb.Items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": 0}})

    def remove_item_policy_by_name(self, item_name, store_name):
        policyId = self.mydb.Items.get_one({"name": item_name, "store": store_name})['policy']
        self.remove_item_policy_by_id(policyId)


    def remove_store(self, store_name):
        collection = self.mydb["Stores"]
        store_to_remove = {"name": store_name}
        collection.delete_one(store_to_remove)
        collection1 = self.mydb["StoreManagers"]
        collection1.delete_many({"store_name": store_name})
        collection2 = self.mydb["StoreOwners"]
        collection2.delete_one({"store_name": store_name})
        collection3 = self.mydb["Items"]
        collection3.delete_many({"store": store_name})
        collection4 = self.mydb["Cart"]
        collection4.delete_many({"store_name": store_name})

    def remove_store_manager(self, manager_name, store_name):
        collection = self.mydb["StoreManagers"]
        manager_to_remove = {"store_name": store_name, "manager": manager_name}
        collection.delete_one(manager_to_remove)

    def remove_store_owner(self, store_name, owner_name):
        collection = self.mydb["StoreOwners"]
        owner_to_remove = {"store_name": store_name, "owner": owner_name}
        collection.delete_one(owner_to_remove)

    def remove_cart(self, user_name, store_name):
        collection = self.mydb["Cart"]
        cart_to_remove = {"user_name": user_name, "store_name": store_name}
        collection.delete_one(cart_to_remove)

    def remove_item_from_cart(self, user_name, store_name, item_name, quantity_to_remove):
        collection = self.mydb["Cart"]
        item_to_remove_from_cart = {"user_name": user_name, "store_name": store_name, "item_name": item_name}
        collection.update_one(item_to_remove_from_cart, {"$inc": {"quantity": quantity_to_remove}})

    def remove_user_notifications(self, user_name):
        collection = self.mydb["UserNotification"]
        notification_to_remove = {"receiver_username": user_name}
        collection.delete_many(notification_to_remove)

    def remove_basket(self, user_name):
        collection = self.mydb["Cart"]
        collection.delete_many({"user_name": user_name})