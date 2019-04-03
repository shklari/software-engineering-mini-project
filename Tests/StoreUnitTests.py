import unittest
from Domain.Store import Store
from Domain.User import User
from Domain.Item import Item
from Domain.Guest import Guest


class StoreUnitTests(unittest.TestCase):

    store = None
    user = None
    item = None
    guest = None

    def setUp(self):
        self.user = User('avokadosh', '112233')
        self.user.logged_in = True
        self.store = Store('Puppies Better', self.user)
        self.item = Item('BaliShag', 20, 'smoke', 'Puppies Better')
        self.guest = Guest()

    def test_add_to_inventory(self):
        self.assertTrue(self.store.add_item_to_inventory(self.user, {'name': self.item.name, 'price': 20, 'category':'smoke'}, 1))
        self.assertTrue(self.store.search_item_by_name(self.item.name).name == self.item.name)
        # check if the item that inserted is in the store inventory
        self.assertFalse(self.store.add_item_to_inventory(self.guest, {'name': self.item.name, 'price': 20, 'category':'smoke'}, 1))
        self.assertFalse(self.store.add_item_to_inventory(self.user, {'name': self.item.name, 'price': 20, 'category':'smoke'}, 0))
        for k in self.store.inventory:
            if k['name'] == self.item.name:
                temp_qn = k['quantity']
        self.assertTrue(self.store.add_item_to_inventory(self.user, {'name': self.item.name, 'price': 20, 'category':'smoke'}, 3))
        for k in self.store.inventory:
            if k['name'] == self.item.name:
                self.assertEqual(temp_qn + 3, k['quantity'])
        print("\n")

    def test_remove_item(self):
        self.store.add_item_to_inventory(self.user, {'name': self.item.name, 'price': 20, 'category': 'smoke'}, 3)
        self.assertTrue(self.store.remove_item_by_quantity(self.user, self.item.name, 2))
        for k in self.store.inventory:
            if k['name'] == self.item.name:
                self.assertTrue(k['quantity'] == 1)
        self.assertFalse(self.store.remove_item_by_quantity(self.user, self.item.name, 2))
        self.assertFalse(self.store.remove_item_by_quantity(self.guest, self.item.name, 2))
        self.assertFalse(self.store.remove_item_from_inventory(self.user, 'bazuka'))
        self.assertTrue(self.store.remove_item_from_inventory(self.user, self.item.name))
        print("\n")

    def test_edit_item_price(self):
        self.store.add_item_to_inventory(self.user, {'name': self.item.name, 'price': 20, 'category': 'smoke'}, 3)
        self.assertTrue(self.store.edit_item_price(self.user, self.item.name, 80))
        for k in self.store.inventory:
            if k['name'] == self.item.name:
                self.assertTrue(k['val'].price == 80)
        self.store.remove_item_from_inventory(self.user, self.item.name)
        self.assertFalse(self.store.edit_item_price(self.user, self.item.name, 30))
        print("\n")

    def test_add_new_owner(self):
        self.assertTrue(self.store.add_new_owner(self.user, User('kushkush', '123456')))
        self.assertTrue(len(self.store.storeOwners) == 2)
        self.assertFalse(self.store.add_new_owner(User('avabash', '02468'), User('baba', '123456')))
        self.assertTrue(len(self.store.storeOwners) == 2)
        self.assertFalse(self.store.add_new_owner(self.user, User('kushkush', '123456')))
        print("\n")

    def test_remove_owner(self):
        temp = User('kushkush', '123456')
        temp.logged_in = True
        self.store.add_new_owner(self.user, temp)
        self.assertFalse(self.store.remove_owner(temp, self.user))
        self.assertFalse(self.store.remove_owner(User('bablu', '111111'), temp))
        self.assertTrue(self.store.remove_owner(self.user, temp))
        flag = True
        for k in self.store.storeOwners:
            if k.username == temp.username:
                flag = False
        self.assertTrue(flag)
        for k in self.store.storeOwners:
            if k.username == self.user.username:
                for x in k.appointees:
                    if x.username == temp.username:
                        flag = False
        self.assertTrue(flag)
        print("\n")

    def test_add_new_manager(self):
        temp = User('kushkush', '123456')
        temp.logged_in = True
        self.assertTrue(self.store.add_new_manager(self.user, temp, None))
        flag = False
        for k in self.store.storeManagers:
            if k.username == temp.username:
                flag = True
        self.assertTrue(flag)
        for k in self.store.storeOwners:
            if k.username == self.user.username:
                for x in k.appointees:
                    if x.username == temp.username:
                        flag = False
        self.assertFalse(flag)
        print("\n")

    def test_remove_manager(self):
        temp = User('kushkush', '123456')
        temp.logged_in = True
        self.store.add_new_manager(self.user, temp, None)
        self.assertFalse(self.store.remove_manager(temp, self.user))
        self.assertFalse(self.store.remove_manager(User('bablu', '111111'), temp))
        self.assertTrue(self.store.remove_manager(self.user, temp))
        flag = True
        for k in self.store.inventory:
            if k.username == temp.username:
                flag = False
        self.assertTrue(flag)
        for k in self.store.storeOwners:
            if k.username == self.user.username:
                for x in k.appointees:
                    if x.username == temp.username:
                        flag = False
        self.assertTrue(flag)
        print("\n")