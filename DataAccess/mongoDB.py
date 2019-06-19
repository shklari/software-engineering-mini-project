import pymongo
from django.utils.datetime_safe import datetime

from Domain.Item import Item
from Domain.Store import Store
from Domain.StoreManager import StoreManager
from Domain.StoreOwner import StoreOwner
from Domain.User import User
from Domain.BuyingPolicy import *


class DB:
    def __init__(self):
        self.policyid = 1
        self.myclient = pymongo.MongoClient("mongodb+srv://grsharon:1234@cluster0-bkvsz.mongodb.net/test?retryWrites=true&w=majority")
        self.mydb = self.myclient["Store"]

    # adder functions

    def parse_item_policy(self, policy, item_name):
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

    def parse_store_policy(self, policy, store_name):
        new_policy = None
        if policy['type'] == 'min':
            new_policy = MinQuantityStorePolicy(store_name, policy['args'])
        elif policy['type'] == 'max':
            new_policy = MaxQuantityStorePolicy(store_name, policy['args'])
        return new_policy

    def add_user(self, user):
        collection = self.mydb["Users"]
        user_to_add = {"name": user.username, "password": user.password, "age": user.age, "country": user.country}
        collection.insert_one(user_to_add)

    def add_store(self, store, username):
        collection = self.mydb["Stores"]
        store_to_add = {"name": store.name, "rank": store.rank, "policy": 0}
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

    def add_item_policy(self, item_name, store_name, policy_type, policy_combo, policy_args, policy_override):
        collection = self.mydb["Policies"]
        fatherson = self.mydb["PolicyComposed"]
        items = self.mydb['Items']
        if policy_override == "true":
            self.remove_item_policy_by_name(item_name, store_name)
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.policyid}})
            collection.insert_one({"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args})
            self.policyid += 1
        else:
            old_policyId = items.find_one({"name": item_name, "store": store_name})['policy']
            new_policy = {"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args}
            comp_policy = {"policyid": self.policyid + 1, "type": "", "combo": policy_combo, "args": ""}
            collection.insert_many([new_policy, comp_policy])
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.policyid + 1}})
            fatherson.insert_many([{"father": self.policyid + 1, "son": old_policyId},
                                   {"father": self.policyid + 1, "son": self.policyid}])
            self.policyid += 2

    def add_notification(self, sender_username, receiver_username, key, message, type):
        collection = self.mydb["UserNotification"]
        not_to_add = {"sender_username": sender_username, "receiver_username": receiver_username,
                      "key": key, "message": message, "type": type}
        collection.insert_one(not_to_add)

    def add_cart(self, user_name, store_name, item_name, quantity, price, category):
        collection = self.mydb["Cart"]
        cart_to_add = {"user_name": user_name, "store_name": store_name, "item_name": item_name,
                       "quantity": quantity, "price": price, "category": category}
        collection.insert_one(cart_to_add)

    def add_policy_to_item(self, item_name, store_name, policy_type, policy_combo, policy_args, policy_override):
        collection = self.mydb["Policies"]
        fatherson = self.mydb["PolicyComposed"]
        items = self.mydb['Items']
        if policy_override == "true":
            self.remove_item_policy_by_name(item_name, store_name)
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.policyid}})
            collection.insert_one({"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args})
            self.policyid += 1
        else:
            old_policyId = items.find_one({"name": item_name, "store": store_name})['policy']
            new_policy = {"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args}
            comp_policy = {"policyid": self.policyid + 1, "type": "", "combo": policy_combo, "args": ""}
            collection.insert_many([new_policy, comp_policy])
            items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": self.policyid + 1}})
            fatherson.insert_many([{"father": self.policyid + 1, "son": old_policyId},
                                   {"father": self.policyid + 1, "son": self.policyid}])
            self.policyid += 2

    def add_policy_to_store(self, store_name, policy_type, policy_combo, policy_args, policy_override):
        collection = self.mydb["Policies"]
        fatherson = self.mydb["PolicyComposed"]
        stores = self.mydb['Store']
        if policy_override == "true":
            self.remove_store_policy_by_name(store_name)
            stores.update_one({"store": store_name}, {"$set": {"policy": self.policyid}})
            collection.insert_one({"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args})
            self.policyid += 1
        else:
            old_policyId = stores.find_one({"name": store_name})['policy']
            new_policy = {"policyid": self.policyid, "type": policy_type, "combo": policy_combo, "args": policy_args}
            comp_policy = {"policyid": self.policyid + 1, "type": "", "combo": policy_combo, "args": ""}
            collection.insert_many([new_policy, comp_policy])
            stores.update_one({"name": store_name}, {"$set": {"policy": self.policyid + 1}})
            fatherson.insert_many([{"father": self.policyid + 1, "son": old_policyId},
                                   {"father": self.policyid + 1, "son": self.policyid}])
            self.policyid += 2

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
            store = self.mydb['Stores'].find_one({"name": store_name})
            policyid = store['policy']
            owners = self.get_store_owners_from_db(store_name)
            managers = self.get_store_managers_from_db(store_name)
            inventory = self.get_store_inventory_from_db(store_name)
            the_store = Store(store_name, owners, inventory)
            the_store.storeManagers = managers
            policy = self.get_store_policy_by_id(policyid, store_name)
            the_store.set_buying_policy(policy)
            return the_store
        return None

    def get_all_stores(self):
        stores = self.mydb.Stores.find({})
        ret_list = []
        for stor in stores:
            store_to_add = self.get_store(stor['name'])
            ret_list.append(store_to_add)
        return ret_list

    def get_quantity_from_cart(self, item_name, store_name):
        return self.mydb.Cart.find_one({"item_name": item_name, "store_name": store_name})['quantity']

    def does_store_exist(self, store_name):
        return True if self.mydb.Stores.count_documents({"name": store_name}) > 0 else False

    def get_item_from_store(self, param, store_name):
        return self.mydb.Items.find({"store": store_name}, {"quantity": {"$gt": 0}},
                                    {"$or": [{"name": param}, {"price": param}, {"category": param}]})

    def get_store_inventory_from_db(self, store_name):
        ret_dict = []
        if self.store_inventory_has_items(store_name):
            curs = self.mydb.Items.find({"store": store_name})
            ret_dict = []
            for item in curs:
                tmpobj = {"name": item['name'], "val": Item(item['name'], item['price'], item['category'],
                                                            item['store']), "quantity": item["quantity"]}
                # "policy": {"type": policy['type'], "combo": policy['combo'],
                #                                         "args": policy['args'], "override": policy['override']}
                policy = self.get_item_policy_by_name(tmpobj['name'], store_name)
                tmpobj['val'].set_buying_policy(policy)
                ret_dict.append(tmpobj)
        return ret_dict
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

    def get_all_products(self):
        items = self.mydb["Items"].find({})
        ret = []
        for item in items:
            obj = {"name": item['name'], "val": Item(item['name'], item['price'],
                                                     item['category'], item['store']), "quantity": item["quantity"]}
            policy = self.get_item_policy_by_name(obj['name'], item['store'])
            obj['val'].set_buying_policy(policy)
            ret.append(obj)
        return ret

    def get_store_owners_from_db(self, store_name):
        curs = self.mydb.StoreOwners.find({"store_name": store_name})
        ret_list = []
        for owner in curs:
            usr = self.get_user(owner['owner'])
            owner_to_add = StoreOwner(usr.username, usr.password, usr.age, usr.country, owner['appointer'])
            ret_list.append(owner_to_add)
        return ret_list

    def get_store_managers_from_db(self, store_name):
        curs = self.mydb.StoreManagers.find({"store_name": store_name})
        ret_list = []
        for manager in curs:
            usr = self.get_user(manager['manager'])
            manager_to_add = StoreManager(usr.username, usr.password, usr.age, usr.country, manager['appointer'],
                                          manager['permission'])
            ret_list.append(manager_to_add)
        return ret_list

    def get_item_policy_by_id(self, policyId, item_name):
        sons = self.mydb.PolicyComposed.find({"father": policyId})
        policy = self.mydb.Policies.find_one({"policyid": policyId})
        if len(sons) == 0:
            return self.parse_item_policy(policy, item_name)
        comp_policy = AndCompositeBuyingPolicy() if policy['combo'] == "true" else OrCompositeBuyingPolicy()
        for iter in sons:
            sonId = iter['son']
            sonpolicy = self.get_item_policy_by_id(sonId, item_name)
            comp_policy.add_policy(sonpolicy)
        return comp_policy

    def get_item_policy_by_name(self, item_name, store_name):
        policyId = self.mydb.Items.find_one({"name": item_name, "store": store_name})['policy']
        if policyId == 0:
            return ItemPolicy()
        return self.get_item_policy_by_id(policyId, item_name)

    def get_store_policy_by_id(self, policyId, store_name):
        if policyId == 0:
            return
        sons = self.mydb.PolicyComposed.find({"father": policyId})
        policy = self.mydb.Policies.find_one({"policyid": policyId})
        if sons.count() == 0:
            return self.parse_store_policy(policy, store_name)
        comp_policy = AndCompositeBuyingPolicy() if policy['combo'] == "true" else OrCompositeBuyingPolicy()
        for iter in sons:
            sonId = iter['son']
            sonpolicy = self.get_store_policy_by_id(sonId, store_name)
            comp_policy.add_policy(sonpolicy)
        return comp_policy

    def get_store_policy_by_name(self, store_name):
        policyId = self.mydb.Stores.find_one({"name": store_name})['policy']
        if policyId == 0:
            return ItemPolicy()
        return self.get_item_policy_by_id(policyId, store_name)

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
                    self.remove_item_policy_by_id(sonId, item_name, store_name)
                fatherson.delete_many({"father": id})
            self.mydb.Policies.delete_one({"policyid": id})
            self.mydb.Items.update_one({"name": item_name, "store": store_name}, {"$set": {"policy": 0}})

    def remove_item_policy_by_name(self, item_name, store_name):
        policyId = self.mydb.Items.get_one({"name": item_name, "store": store_name})['policy']
        self.remove_item_policy_by_id(policyId, item_name, store_name)

    def remove_store_policy_by_id(self, id, store_name):
        fatherson = self.mydb.PolicyComposed
        if id > 0:
            sons = fatherson.find({"father": id})
            if sons.count() > 0:
                for son in sons:
                    sonId = son['son']
                    self.remove_item_policy_by_id(sonId, store_name)
                fatherson.delete_many({"father": id})
            self.mydb.Policies.delete_one({"policyid": id})
            self.mydb.Items.update_one({"name": store_name}, {"$set": {"policy": 0}})

    def remove_store_policy_by_name(self, store_name):
        policyId = self.mydb.Stores.get_one({"name": store_name})['policy']
        self.remove_store_policy_by_id(policyId, store_name)

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

    def get_bascket_db(self, username):
        items = self.mydb.Cart.find({"user_name": username})
        ret_list = []
        for itm in items:
            itm_to_add = Item(itm['item_name'], itm['price'], itm['category'], itm['store_name'])
            ret_list.append(itm_to_add)
        return ret_list
