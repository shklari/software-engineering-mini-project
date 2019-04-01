from Domain.User import User
from Domain.Guest import Guest
from Domain.Store import Store
from Domain.StoreOwner import StoreOwner
from Domain.SystemManager import SystemManager


class System:

    def __init__(self):
        self.system_manager = 0
        self.cur_user = 0
        self.users = {}
        self.stores = []

    def init_system(self, system_manager_user_name, system_manager_password):
        if not self.sign_up(system_manager_user_name, system_manager_password):
            return None
        manager = SystemManager(system_manager_user_name, system_manager_password)
        self.users[manager.username] = manager
        self.system_manager = manager
        self.cur_user = Guest()
        return self.cur_user

    def sign_up(self, username, password):
        if username in self.users:
            print("This user name is taken")
            return False
        if password is None:
            print("Password can not be empty")
            return False
        else:
            new_user = User(username, password)
            self.users[username] = new_user
            print("Welcome, new user {}! You may now log in".format(username))
            return True

    def login(self, username, password):
        if username not in self.users:
            print("No such user")
            return False
        user_to_check = self.users[username]
        if user_to_check.logged_in:
            print("You are already logged in")
            return False
        elif user_to_check.password != password:
            print("Wrong password")
            return False
        else:
            user_to_check.logged_in = True
            self.cur_user = user_to_check
            print("Hey {}! You are now logged in".format(username))
            return True

    def logout(self):
        if not self.cur_user.logged_in:
            print("You can't log out until you log in")
            return False
        else:
            self.cur_user.logged_in = False
            new_user = Guest()
            self.cur_user = new_user
            print("You are now logged out")
            return True

    def search(self, param):
        ret_list = []
        for s in self.stores:
            ret_list.append(s.search_item_by_name(param))
            ret_list.append(s.search_item_by_category(param))
            ret_list.append(s.search_item_by_price(param))

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

    def buy_items(self, items):
        flag = False
        for item in items:
            flag = self.cur_user.buy_item(item)
            # if false then stop the purchase
        return flag

    def create_store(self, store_name):
        if isinstance(self.cur_user, User) and store_name not in self.stores:
            new_store = Store(store_name)
            new_store.storeOwners.append(StoreOwner(self.cur_user.username, self.cur_user.password))
            self.stores.append(new_store)
            return new_store
        return False

    def remove_user(self, username):
        if not isinstance(self.cur_user, SystemManager):
            print("You can't remove a user, you are not the system manager")
            return False
        user_to_remove = self.users[username]
        stores_to_remove = []
        for store in self.stores:
            if len(store.storeOwners) == 1 and user_to_remove.username == store.storeOwners[0].username:
                stores_to_remove.append(store)
        for st in stores_to_remove:
            self.stores.remove(st)
        del self.users[username]
        print("System manager removed the user {}".format(username))
        return True


if __name__ == '__main__':
    amazon = System()
    amazon.init_system('shaioz', 1234)
    amazon.sign_up('ava bash', 666)
    amazon.login('ava bash', 666)
    amazon.create_store('zara')
    amazon.create_store('pnb')
    amazon.logout()
    amazon.login('shaioz', 1234)
    amazon.create_store('shais store')
    print("Stores are:")
    for s in amazon.stores:
        print(s.name)
    print("Users are:")
    for u in amazon.users:
        print(amazon.users[u].username)
    amazon.remove_user('ava bash')
    print("Stores are:")
    for s in amazon.stores:
        print(s.name)
    print("Users are:")
    for u in amazon.users:
        print(u)