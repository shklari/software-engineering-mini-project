from .User import User
from .Client import Client


class System:

    def __init__(self, system_manager):
        self.sys_manager = system_manager
        self.cur_user = User()
        self.clients = dict.fromkeys(['username', 'client'])
        self.stores = []

    def sign_up(self, username, password):
        if self.clients[username] is not None:
            print("This user name is taken")
            return False
        if password is None:
            print("Password can not be empty")
            return False
        else:
            new_client = Client(username, password)
            self.clients[username] = new_client
            return True

    def login(self, username, password):
        if isinstance(self.cur_user, Client):
            print("You are already logged in")
            return False
        client_to_check = self.clients[username]
        if client_to_check is None:
            print("No such user")
            return False
        elif client_to_check.password != password:
            print("Wrong password")
            return False
        else:
            self.cur_user = client_to_check
            return client_to_check

    def logout(self):
        if not isinstance(self.cur_user, Client):
            print("You can't log out until you log in")
            return False
        else:
            new_user = User()
            self.cur_user = new_user
            return new_user

    def search(self, param):
        ret_list = []
        for s in self.stores:
            ret_list += s.search_item_by_name(param)
            ret_list += s.search_item_by_category(param)
            ret_list += s.search_item_by_price(param)

        return ret_list

    def buy_items(self, items):
        flag = False
        for item in items:
            flag = self.cur_user.buy_item(item)
        return flag

    def create_store(self, name): pass

    def remove_client(self, client): pass