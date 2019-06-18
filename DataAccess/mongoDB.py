import pymongo


class DB:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb+srv://grsharon:1234@cluster0-bkvsz.mongodb.net/test?retryWrites=true&w=majority")
        self.mydb = self.myclient["Store"]

    def add_user(self, user):
        collection = self.mydb["Users"]
        user_to_add = {"name": user.username, "password": user.password, "age": user.age, "country": user.country}
        collection.insert_one(user_to_add)

    def add_store(self, store):
        collection = self.mydb["Stores"]
        store_to_add = {"name": store.name, "rank": store.rank}
        collection.insert_one(store_to_add)

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
    def add_item(self, item, quantity, policy):
        collection = self.mydb["Items"]
        item_to_add = {"name": item.name, "store": item.store_name, "price": item.price, "category": item.category,
                       "quantity": quantity, "policy": {"type": policy.type, "combo": policy.combo, "args": policy.args,
                                                        "override": policy.override}}
        collection.insert_one(item_to_add)

    def add_notification(self, sender_username, receiver_username, key, message):
        collection = self.mydb["UserNotification"]
        not_to_add = {"sender_username": sender_username, "receiver_username": receiver_username,
                      "key": key, "message": message}
        collection.insert_one(not_to_add)

    def add_cart(self, user_name, store_name, item_name, quantity):
        collection = self.mydb["Cart"]
        cart_to_add = {"user_name": user_name, "store_name": store_name, "item_name": item_name, "quantity": quantity}
        collection.insert_one(cart_to_add)

    def add_policy_to_item(self, store_name, item_name, new_policy): pass
    # TODO: set new policy to an item

    def add_policy_to_store(self, store_name, new_policy): pass
    # TODO: set new policy to a store

    def get_user(self, user_name):
        return self.mydb.Users.find({"name": user_name})

    def get_store(self, store_name):
        return self.mydb.Stores.find({"name": store_name})

    def get_item_from_store(self, param, store_name):
        return self.mydb.Items.find({"store": store_name}, {"quantity": {"$gt": 0}},
                                    {"$or": [{"name": param}, {"price": param}, {"category": param}]})

    def get_inventory_from_db(self):
        return self.mydb.Items.find()

    def get_all_stores_from_db(self):
        return self.mydb.Stores.find()

    def edit_item_price_in_db(self, store_name, item_name, new_price): pass
    # TODO

    def edit_item_quantity_in_db(self, store_name, item_name, new_quantity): pass
    # TODO

