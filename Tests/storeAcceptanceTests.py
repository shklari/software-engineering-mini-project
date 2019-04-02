import unittest
from Service.serviceBridge import ServiceBridge


class TestStore(unittest.TestCase):

    service = ServiceBridge()
    store1 = None
    store2 = None
    manager = None
    owner = None
    items = []
    user = None

    # store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
    # user {'username'}
    def setUp(self):
        self.owner = {'name': 'Joseph'}
        self.manager = {'name': 'Itay', 'password': '123456'}
        self.store1 = {'name': 'EL', 'storeManagers': [], 'inventory': [], 'storeOwners': [], 'rank': 3}
        self.store2 = {'name': 'Fox', 'storeManagers': [], 'inventory': [], 'storeOwners': [], 'rank': 2}
        self.store1['storeManagers'] = [self.manager]
        self.store1['storeOwners'] = [self.owner]
        item1 = {'name': 'iphone7', 'price': 3000, 'rank': 5, 'category': 'Electrics'}
        item2 = {'name': 'Tv', 'price': 2000, 'rank': 4, 'category': 'Electrics'}
        item3 = {'name': 'pillow', 'price': 50, 'rank': 1, 'category': 'Home'}
        self.store1['inventory'] = self.items
        self.items = [item1, item2, item3]
        self.user = {'basket': []}
        self.store2['storeManagers'] = self.manager
        self.store2['storeOwners'] = self.owner
        self.store2['inventory'] = [item1, item2]

    def test_createStore(self):# 3.2
        store = self.service.create_store(self.store1['name'])
        self.assertEqual(store['name'], self.store1['name'], 'create store failed')

    def test_addToCartTest(self):# 2.6
        result = self.service.add_to_cart(self.user, self.store1['name'], self.items[0]) #store name
        self.assertTrue(result, 'add to cart failed')
        # cart = self.service.get_cart(self.user, self.store1["name"])
        item = self.service.get_Item_From_Cart(self.store1["name"], self.items[0]["name"])
        self.assertEqual(item, self.items[0]['name'], 'add to cart failed')
        newitem = {'name': 'undefined', 'price': 0, 'rand': 5, 'category': 'undefined'}
        result = self.service.add_to_cart(self.store1['name'], newitem)
        self.assertTrue(result, 'add to cart failed')
        item = self.service.get_Item_From_Cart(self.store1["name"], newitem['name'])
        self.assertEqual(item, self.items[0]['name'], 'add to cart failed')

    def test_addItemToInventory(self):# 4.1.1 [{'name': iphone , 'quantity': 2}]
        inventory = self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2)
        self.assertNotEqual(inventory, False, 'add item to inventory failed')
        ans = [item for item in inventory if item['name'] == self.items[0]['name']]
        self.assertEqual(len(ans), 1, 'many items with same name in inventory!')
        self.assertEqual(ans[0]['name'], self.items[0]['name'], 'add item to inventory failed')
        self.assertEqual(ans[0]['quantity'], 2, 'add item to inventory failed')

    def test_removeItemFromInventory(self):  # 4.1.2
        inventory = self.service.remove_item_from_inventory(self.items[0]['name'], self.store1['name'], 2)
        self.assertNotEqual(inventory, False, 'remove item from inventory failed')
        ans = [item for item in inventory if item['name'] == self.items[0]['name']]
        self.assertEqual(len(ans), 0, 'remove item from inventory failed')

    def test_editItemFromInventory(self):  # 4.1.3
        self.service.add_item_to_inventory(self.items[0], self.store1, 2)
        item = self.service.edit_item_price(self.store1['name'], self.items[0]['name'], 100)
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')

    def test_add_new_owner(self):  # 4.3
        store = self.service.add_new_owner(self.owner['name'])
        self.assertNotEqual(store, False, 'add new owner failed')
        self.assertTrue({'username': self.manager['name']} in store['storeOwners'], 'add new owner failed')
        result = self.service.add_new_owner(self.owner['name'])
        self.assertFalse(result, 'add new owner failed')

    def test_remove_owner(self):  # 4.4
        store = self.service.remove_owner(self.owner['name']) # based on add new owner
        self.assertNotEqual(store, False, 'remove owner failed')
        self.assertTrue({'username': self.owner['name']} not in store['storeOwners'], 'remove owner failed')
        result = self.service.remove_owner(self.user['name'])
        self.assertFalse(result, 'remove owner failed')

    def test_add_new_manager(self):  # 4.5
        permissions = {'Edit': False, 'Remove': False, 'Add': True}
        store = self.service.add_new_manager(self.manager['name'], permissions)
        self.assertNotEqual(store, False, 'add new manager failed')
        self.assertTrue({'username': self.manager['name']} in store['storeManagers'], 'add new manager failed')

    def remove_manager(self):  # 4.6
        permissions = {'Edit': False, 'Remove': False, 'Add': True}
        store = self.service.remove_manager(self.manager['name'], permissions)
        self.assertNotEqual(store, False, 'add new manager failed')
        self.assertTrue({'username': self.manager['name']} not in store['storeManagers'], 'remove manager failed')


if __name__ == '__main__':
    unittest.main()
