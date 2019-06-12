from Service.service import ServiceInterface
from Domain.System import System
from Domain.Response import ResponseObject
from .RealTimeAlert import RealTimeAlert


class ServiceImpl(ServiceInterface):

    def __init__(self):
        self.sys = System()
        self.guests = []
        self.users = []
        self.admins = []
        self.ownersAlert = RealTimeAlert(self)

    # assumes the init function receives the username and password of the system manager
    def init(self, sm_username, sm_password, system_manager_age, system_manager_country):
        result = self.sys.init_system(sm_username, sm_password, system_manager_age, system_manager_country)
        if result.success:
            return ResponseObject(True, result.value, "System initialized successfully")
        else:
            return ResponseObject(False, False, "System failed to initialize\n" + result.message)

    def sign_up(self, username, password, age, country):
        result = self.sys.sign_up(username, password, age, country)
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

    def logout(self, username):
        result = self.sys.logout(username)
        if result.success:
            return result
        else:
            return ResponseObject(False, False, "Logout failed.\n" + result.message)

    def create_store(self, store_name, username):
        result = self.sys.create_store(store_name, username)
        if not result.success:
            return ResponseObject(False, None, "Could not create store \'" + store_name + "\'\n" + result.message)
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

    # changed 'username' to 'user_to_remove'
    def remove_user(self, user_to_remove, username):
        result = self.sys.remove_user(user_to_remove)
        if not result.success:
            return ResponseObject(False, False, "Can't remove user\n" + result.message)
        else:
            return result

    def get_cart(self, store_name, username):
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        result = curr_user.get_cart(store_name)
        if not result.success:
            return result
        cart = result.value
        return ResponseObject(True, {'store_name': cart.store_name, 'items_and_quantities': cart.items_and_quantities}, "")

    def get_basket(self, username):
        return self.sys.get_basket(username)

    def get_basket_subtotal(self, username):
        subtotal = 0
        basket = self.sys.get_basket(username)
        if basket.success:
            for cart in basket.value:
                for item in cart['cart']:
                    subtotal += item['price'] * item['quantity']
        return ResponseObject(True, {'subtotal': subtotal}, "")

    def get_basket_size(self, username):
        return self.sys.get_basket_size(username)

    def add_to_cart(self, store_name, item_name, quantity, username):
        result = self.sys.add_to_cart(store_name, item_name, quantity, username)
        if not result.success:
            return ResponseObject(False, False, "Can't add item " + item_name + " to cart " + store_name + "\n" + result.message)
        curr_user = self.sys.get_user_or_guest(username).value
        cart_result = curr_user.get_cart(store_name)
        cart = cart_result.value
        added = cart.items_and_quantities.get(item_name)
        return ResponseObject(True, added, "Item " + item_name + " added successfully to cart " + store_name)

    def remove_from_cart(self, store_name, item_name, username):
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        result = curr_user.remove_from_cart(store_name, item_name)
        if not result.success:
            return ResponseObject(False, False, "Can't remove item " + item_name + " from cart " + store_name + "\n" + result.message)
        return ResponseObject(True, curr_user.get_cart(store_name).value.items_and_quantities, "Item " + item_name + " removed from cart " + store_name)

    def buy_items(self, items, username):
        result = self.sys.buy_items(items)
        if not result.success:
            return ResponseObject(False, False, "Can't buy requested items. Transaction cancelled\n" + result.message)
        return ResponseObject(True, True, "Transaction succeeded. Items removed from basket\n" + result.message)

    # item ::= {'name': string, 'price': int, 'category': string, 'store_name': string}
    def add_item_to_inventory(self, item, store_name, quantity, username):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't add items to store " + store_name + "\n" + store_result.message)
        store = store_result.value
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        add = store.add_item_to_inventory(curr_user, item, quantity)
        if not add.success:
            return ResponseObject(False, False, "Error: can't add item " + item['name'] + " to store " + store_name + "\n" + add.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, inv, "Item " + item['name'] + " added successfully to " + store_name + " inventory")

    def remove_item_from_inventory(self, item_name, store_name, username):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't remove items from store " + store_name + "\n" + store_result.message)
        store = store_result.value
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        remove = store.remove_item_from_inventory(curr_user, item_name)
        if not remove.success:
            return ResponseObject(False, False, "Error: can't remove item " + item_name + " from store " + store_name + "\n" + remove.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, inv, "Item " + item_name + " removed from " + store_name + " inventory")

    def edit_product(self, itemname, store_name, quantity, price, username):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False,
                                  "Error: can't add items to store " + store_name + "\n" + store_result.message)
        store = store_result.value
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        item = store.search_item_by_name(itemname)
        if not item:
            return ResponseObject(False, False,
                                  "Error: no such product in " + store_name + "store\n" + store_result.message)
        add = store.add_item_to_inventory(curr_user, {'name': itemname, 'price': price, 'category': ''}, quantity)
        if not add.success:
            return ResponseObject(False, False, "Error: can't add item " + itemname[
                'name'] + " to store " + store_name + "\n" + add.message)
        if price > 0:
            add = store.edit_item_price(curr_user, itemname, price)
            if not add.success:
                return ResponseObject(False, False, "Error: can't edit " + itemname[
                    'name'] + "'s price in" + store_name + "store\n" + add.message)
        inv = []
        for i in store.inventory:
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, inv, "Item " + itemname + " edited successfully in " + store_name + " inventory")

    def decrease_item_quantity(self, store_name, item_name, quantity, username):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't remove items from store " + store_name + "\n" +
                                  store_result.message)
        store = store_result.value
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        decrease = store.remove_item_by_quantity(curr_user, item_name, quantity)
        if not decrease.success:
            return ResponseObject(False, False, "Can't change quantity of item " + item_name + "\n" + decrease.message)
        inv = []
        for i in store.inventory:
            if i['name'] == item_name:
                if i['quantity'] == 0:
                    self.ownersAlert.notify(store.storeOwners, "item " + item_name + " is out of stock!")
            inv.append({'name': i['name'], 'quantity': i['quantity']})
        return ResponseObject(True, inv, "The quantity of item " + item_name + " was successfully decreased")

    def edit_item_price(self, store_name, item_name, new_price, username):
        store_result = self.sys.get_store(store_name)
        if not store_result.success:
            return ResponseObject(False, False, "Error: can't edit items in store " + store_name + "\n" + store_result.message)
        store = store_result.value
        find_user = self.sys.get_user_or_guest(username)
        if not find_user.success:
            return find_user
        curr_user = find_user.value
        edit = store.edit_item_price(curr_user, item_name, new_price)
        if not edit.success:
            return ResponseObject(False, False, "Error: can't edit item " + item_name + " in store " + store_name + "\n" + edit.message)
        ret = store.search_item_by_name(item_name)
        if not ret:
            return ResponseObject(False, False, "Error: item " + item_name + "doesn't exist in this store's inventory")
        return ResponseObject(True, {'name': ret.name, 'price': ret.price, 'category': ret.category}, "The price of item " + item_name + " was successfully changed")

    def add_new_owner(self, store_name, new_owner, username):
        result = self.sys.add_owner_to_store(store_name, new_owner, username)
        if not result.success:
            return ResponseObject(False, False, "Can't add new owner " + new_owner + " to store " + store_name + "\n" + result.message)
        self.ownersAlert.notify([new_owner], "you are now an owner of " + store_name + "store")
        store = self.sys.get_store(store_name).value  # already checked if store exists in add_owner_to_store in system
        owners = []
        for o in store.storeOwners:
            owners.append({'username': o.username})
        return ResponseObject(True, {'name': store_name, 'storeOwners': owners}, "New owner " + new_owner +
                              " added successfully to store " + store_name)

    def add_new_manager(self, store_name, new_manager, permissions, username):
        result = self.sys.add_manager_to_store(store_name, new_manager, permissions, username)
        if not result.success:
            return ResponseObject(False, False, "Can't add new manager " + new_manager + " to store " + store_name + "\n" + result.message)
        self.ownersAlert.notify([new_manager], "you are now a manager of " + store_name + "store")
        store = self.sys.get_store(store_name).value
        managers = []
        for m in store.storeManagers:
            managers.append({'username': m.username})
        return ResponseObject(True, {'name': store_name, 'storeManagers': managers}, "New manager " + new_manager + " added successfully to store " + store_name)

    def remove_owner(self, store_name, owner_to_remove, username):
        result = self.sys.remove_owner_from_store(store_name, owner_to_remove, username)
        if not result.success:
            return ResponseObject(False, False, "Can't remove owner " + owner_to_remove + " from store " + store_name + "\n" + result.message)
        self.ownersAlert.notify([owner_to_remove], "you are no longer store owner of " + store_name + "store")
        store = self.sys.get_store(store_name).value
        owners = []
        for o in store.storeOwners:
            owners.append({'username': o.username})
        return ResponseObject(True, {'name': store_name, 'storeOwners': owners}, "Owner " + owner_to_remove +
                              " was successfully removed from the store's owners")

    def remove_manager(self, store_name, manager_to_remove, username):
        result = self.sys.remove_manager_from_store(store_name, manager_to_remove, username)
        if not result.success:
            return ResponseObject(False, False, "Can't remove manager " + manager_to_remove +
                                  " from store " + store_name + "\n" + result.message)
        self.ownersAlert.notify([manager_to_remove], "you are no longer manager owner of " + store_name + "store")
        store = self.sys.get_store(store_name).value
        managers = []
        for m in store.storeManagers:
            managers.append({'username': m.username})
        return ResponseObject(True, {'name': store_name, 'storeManagers': managers}, "Manager " + manager_to_remove +
                              " removed successfully from the store's managers")

    def shop_all(self):
        items_list = self.sys.get_total_system_inventory()
        if len(items_list.value) == 0:
            return ResponseObject(False, [], "No items in the system")
        return ResponseObject(True, items_list.value, "")

    def get_store(self, store_name):
        store = self.sys.get_store(store_name)
        return store

    def get_stores(self):
        stores = self.sys.get_stores()
        res = []
        for store in stores:
            res.append({'name':store.name})
        return ResponseObject(True, {'stores':res}, "")