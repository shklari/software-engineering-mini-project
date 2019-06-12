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

    def add_store_manager(self, store_name, user_name, appointer, is_remove_per, is_edit_per, is_add_per):
        collection = self.mydb["StoreManagers"]
        store_manager_to_add = {"store_name": store_name, "manager": user_name, "appointer": appointer,
                                "add_permission": is_add_per, "edit_permission": is_edit_per,
                                "remove_permission": is_remove_per}
        collection.insert_one(store_manager_to_add)

    def add_item(self, item, quantity):
        collection = self.mydb["Items"]
        item_to_add = {"name": item.name, "store": item.store_name, "price": item.price, "category": item.category,
                       "quantity": quantity}
        collection.insert_one(item_to_add)

    def add_notification(self, user_name, time, message):
        collection = self.mydb["UserNotification"]
        not_to_add = {"user_name": user_name, "time": time, "message": message}
        collection.insert_one(not_to_add)
