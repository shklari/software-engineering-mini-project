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

    def add_store_manager(self, store_name, user_name, appointer):
        collection = self.mydb["StoreManagers"]
        store_manager_to_add = {"store_name": store_name, "manager": user_name, "appointer": appointer}
        collection.insert_one(store_manager_to_add)

    def add_store_manager_permissions(self, manager_name, permis):
        collection = self.mydb["StoreManagerPermissions"]
        manager_permis_to_add = {"manager_name": manager_name, "permission": permis}
        collection.insert_one(manager_permis_to_add)

    # def add_item(self, item_name, price, category, store_name):