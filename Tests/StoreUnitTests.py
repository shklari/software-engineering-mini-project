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
        self.item = Item('BaliShag', 20, 'smoke')
        self.guest = Guest()

    def test_add_to_inventory(self):
        self.assertTrue(self.store.add_item_to_inventory(self.user, self.item.name, 1))
        # self.assertEqual(self.store.search_item_by_name(self.item.name), self.item)
        # check if the item that inserted is in the store inventory
        # self.assertFalse(self.store.add_item_to_inventory(self.guest, self.item, 1))
        # self.assertFalse(self.store.add_item_to_inventory(self.user, self.item, 0))
        # for k in self.store.inventory:
        #     if k['name'] == self.item.name:
        #         temp_qn = k['quantity']
        # self.assertTrue(self.store.add_item_to_inventory(self.user, self.item.name, 3))
        # for k in self.store.inventory:
        #     if k['name'] == self.item.name:
        #         self.assertEqual(temp_qn + 3, k['quantity'])
