from Service.service import ServiceInterface
from Domain.System import System
from Domain.Response import ResponseObject


class ServiceImpl(ServiceInterface):

    def __init__(self):
        self.sys = System()

    # assumes the init function receives the username and password of the system manager
    def init(self, sm_username, sm_password):
        result = self.sys.init_system(sm_username, sm_password)
        if result.success:
            return ResponseObject(True, result.value, "System initialized successfully")
        else:
            return ResponseObject(False, False, "System failed to initialize\n" + result.message)

    def sign_up(self, username, password):
        result = self.sys.sign_up(username, password)
        if result.success:
            return ResponseObject(True, True, "Signed up successfully \n" + result.message)
        else:
            return ResponseObject(False, False, "Sign up failed \n" + result.message)

    def login(self, username, password):
        result = self.sys.login(username, password)
        if result.success:
            return result
        else:
            return ResponseObject(False, False, "Login failed.\n" + result.message)

    def search(self, keyword):
        items_list = self.sys.search(keyword)
        if len(items_list) == 0:
            return ResponseObject(False, [], "No item matching the search")
        output_list = []
        for item in items_list:
            print(item)
            output_list.append({'name': item.name, 'price': item.price, 'category': item.category})
        return ResponseObject(True, output_list, "")

    def logout(self):
        result = self.sys.logout()
        if result.success:
            return result
        else:
            return ResponseObject(False, False, "Logout failed.\n" + result.message)

    def create_store(self, name):
        result = self.sys.create_store(name)
        if not result.success:
            return ResponseObject(False, None, "Could not create store \'" + name + "\'\n" + result.message)
        else:
            created = result.value
            message = "New store created.\nName: " + created.name + "\nOwners: "
            sowners = ""
            for o in created.storeOwners:
                sowners += o.username + ", "
            message += sowners
            owners = []
            for o in created.storeOwners:
                owners.append({'username': o.username})
            return ResponseObject(True, {'name': created.name, 'storeOwners': owners}, message)

    def remove_user(self, username):
        result = self.sys.remove_user(username)
        if not result.success:
            return ResponseObject(False, False, "Can't remove user\n" + result.message)
        else:
            return result

    def get_cart(self, store_name):
        curr_user = self.sys.get_cur_user()
        result = curr_user.get_cart(store_name)
        if not result.success:
            return result
        cart = result.value
        for i in cart.keys():
            print("Item name: " + i + "quantity: " + cart[i])
        return ResponseObject(True, cart.items_and_quantities, "")

    def add_to_cart(self, store_name, item_name, quantity):
        result = self.sys.add_to_cart(store_name, item_name, quantity)
        if not result.success:
            return ResponseObject(False, False, "Can't add item " + item_name + " to cart " + store_name + "\n" + result.message)
        curr_user = self.sys.get_cur_user()
        cart_result = curr_user.get_cart(store_name)
        if not cart_result.success:
            return ResponseObject(False, False, "Can't add item " + item_name + " to cart " + store_name + "\n" + cart_result.message)
        cart = cart_result.value
        return ResponseObject(True, cart.items_and_quantities, "Item " + item_name + " added successfully to cart " + store_name)

    def remove_from_cart(self, store_name, item_name):
        curr_user = self.sys.get_cur_user()
        result = curr_user.remove_from_cart(store_name, item_name)
        if not result.success:
            return ResponseObject(False, False, "Can't remove item " + item_name + " from cart " + store_name + "\n" + result.message)
        return ResponseObject(True, curr_user.get_cart().items_and_quantities, "Item " + item_name + " removed from cart " + store_name)

    def buy_items(self, items):
        result = self.sys.buy_items(items)
        if not result.success:
            return ResponseObject(False, False, "Can't buy requested items. Transaction cancelled\n" + result.message)
        return ResponseObject(True, True, "Transaction succeeded. Items removed from basket\n" + result.message)

    # item ::= {'name': string, 'price': int, 'category': string, 'store_name': string}
    def add_item_to_inventory(self, item, store_name, quantity):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't add items to store " + store_name + "\n" + store_result.message)
        store = store_result.value
        user = self.sys.get_cur_user()
        if user is None:
            return ResponseObject(False, False, "Error: no current user")
        add = store.add_item_to_inventory(user, item, quantity)
        if not add.success:
            return ResponseObject(False, False, "Error: can't add item " + item['name'] + " to store " + store_name + "\n" + add.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, inv, "Item " + item['name'] + " added successfully to " + store_name + " inventory")

    def remove_item_from_inventory(self, item_name, store_name):
        store_result = self.sys.get_store(store_name)
        if not store_result:
            return ResponseObject(False, False, "Error: can't remove items from store " + store_name + "\n" + store_result.message)
        store = store_result.value
        user = self.sys.get_cur_user()
        if user is None:
            return ResponseObject(False, False, "Error: no current user")
        remove = store.remove_item_from_inventory(user, item_name)
        if not remove.success:
            return ResponseObject(False, False, "Error: can't remove item " + item_name + " from store " + store_name + "\n" + remove.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, True, "Item " + item_name + " removed from " + store_name + " inventory")

    def decrease_item_quantity(self, store_name, item_name, quantity):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't remove items from store " + store_name + "\n" + store_result.message)
        store = store_result.value
        user = self.sys.get_cur_user()
        if user is None:
            return ResponseObject(False, False, "Error: no current user")
        decrease = store.remove_item_by_quantity(user, item_name, quantity)
        if not decrease.success:
            return ResponseObject(False, False, "Can't change quantity of item " + item_name + "\n" + decrease.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, True, "The quantity of item " + item_name + " was successfully decreased")

    def edit_item_price(self, store_name, item_name, new_price):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't edit items in store " + store_name + "\n" + store_result.message)
        store = store_result.value
        user = self.sys.get_cur_user()
        if user is None:
            return ResponseObject(False, False, "Error: no current user")
        edit = store.edit_item_price(user, item_name, new_price)
        if not edit.success:
            return ResponseObject(False, False, "Error: can't edit item " + item_name + " in store " + store_name + "\n" + edit.message)
        ret = store.search_item_by_name(item_name)
        if not ret:
            return ResponseObject(False, False, "Error: item " + item_name + "doesn't exist in this store's inventory")
        return ResponseObject(True, {'name': ret.name, 'price': ret.price, 'category': ret.category}, "The price of item " + item_name + " was successfully changed")

    def add_new_owner(self, store_name, new_owner):
        result = self.sys.add_owner_to_store(store_name, new_owner)
        if not result.success:
            return ResponseObject(False, False, "Can't add new owner " + new_owner + " to store " + store_name + "\n" + result.message)
        store = self.sys.get_store(store_name).value
        owners = []
        for o in store.storeOwners:
            owners.append({'username': o.username})
        return ResponseObject(True, {'name': store_name, 'storeOwners': owners}, "New owner " + new_owner + " added successfully to store " + store_name)

    def add_new_manager(self, store_name, new_manager, permissions):
        if not self.sys.add_manager_to_store(store_name, new_manager, permissions):
            print("Can't add new manager " + new_manager + " to store " + store_name)
            return False
        store = self.sys.get_store(store_name)
        managers = []
        for m in store.storeManagers:
            managers.append({'username': m.username})
        return {'name': store_name, 'storeManagers': managers}

    def remove_owner(self, store_name, owner_to_remove):
        if not self.sys.remove_owner_from_store(store_name, owner_to_remove):
            print("Can't remove owner " + owner_to_remove + " from store " + store_name)
            return False
        store = self.sys.get_store(store_name)
        owners = []
        for o in store.storeOwners:
            owners.append({'username': o.username})
        return {'name': store_name, 'storeOwners': owners}

    def remove_manager(self, store_name, manager_to_remove):
        if not self.sys.remove_manager_from_store(store_name, manager_to_remove):
            print("Can't remove manager " + manager_to_remove + " from store " + store_name)
            return False
        store = self.sys.get_store(store_name)
        managers = []
        for m in store.storeManagers:
            managers.append({'username': m.username})
        return {'name': store_name, 'storeManagers': managers}

