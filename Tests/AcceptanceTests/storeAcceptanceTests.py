import unittest

from Service.serviceBridge import ServiceBridge


class TestStore(unittest.TestCase):

    service = ServiceBridge()
    store1 = None
    store2 = None
    manager = None
    sys_manager = None
    owner = None
    items = []
    user = None
    system = None

    # def __init__(self):
    #     self.service.create_store()
    # # store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
    # user {'username'}
    def setUp(self):
        self.owner = {'name': 'Joseph', 'password': '123'}
        self.sys_manager = {'name': 'shaioz', 'password': '123456'}
        self.service.init(self.sys_manager['name'], self.sys_manager['password'])
        self.service.login(self.sys_manager['name'], self.sys_manager['password'])
        #self.system = self.service.init(self.sys_manager['name'], self.sys_manager['password'])
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
        self.service.create_store(self.store1['name'])
        self.service.sign_up(self.owner['name'], self.owner['password']) # must be removed in tearDown
        self.service.sign_up(self.manager['name'], self.manager['password'])  # must be removed in tearDown

    def tearDown(self):
        self.service.remove_user(self.owner['name'])
        self.service.remove_user(self.manager['name'])
        self.service.remove_item_from_inventory(self.items[0]['name'], self.store1['name'])
        #self.service.remove_owner(self.store1['name'], self.owner['name'])
        #self.service.remove_manager(self.store1['name'], self.manager['name'])

    def test_createStore(self):# 3.2
        print('create')
        store = self.service.create_store(self.store2['name']).value
        self.assertEqual(store['name'], self.store2['name'], 'create store failed')

    def test_addItemToInventory(self):# 4.1.1 [{'name': iphone , 'quantity': 2}]
        print('add')
        inventory = self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2)
        self.assertNotEqual(inventory.success, False, 'add item to inventory failed')
        ans = [item for item in inventory.value if item['name'] == self.items[0]['name']]
        self.assertEqual(len(ans), 1, 'many items with same name in inventory!')
        self.assertEqual(ans[0]['name'], self.items[0]['name'], 'add item to inventory failed')
        self.assertEqual(ans[0]['quantity'], 2, 'add item to inventory failed')

    def test_removeItemFromInventory(self):  # 4.1.2
        self.assertNotEqual(False, self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2).success)
        inventory = self.service.remove_item_from_inventory(self.items[0]['name'], self.store1['name'])
        self.assertNotEqual(inventory.success, False, 'remove item from inventory failed')
        ans = [item for item in inventory.value if item['name'] == self.items[0]['name']]
        self.assertEqual(len(ans), 0, 'remove item from inventory failed')

    def test_editItemFromInventory(self):  # 4.1.3
        self.assertNotEqual(False, self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2).success)
        #self.service.add_item_to_inventory(self.items[0], self.store1, 2)
        item = self.service.edit_item_price(self.store1['name'], self.items[0]['name'], 100).value
        self.assertEqual(item['price'], 100, 'edit item from inventory failed')

    def test_decrease_item_quantity(self):  # 4.1.3
        self.assertNotEqual(False, self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2).success)
        inventory = self.service.decrease_item_quantity(self.store1['name'], self.items[0]['name'], 1)
        self.assertNotEqual(inventory.success, False, 'edit item from inventory failed')
        ans = [item for item in inventory.value if item['name'] == self.items[0]['name']]
        self.assertNotEqual(len(ans), 0, 'edit item from inventory failed')
        self.assertEqual(ans[0]['quantity'], 1, 'edit item from inventory failed')

    def test_add_new_owner(self):  # 4.3
        #result = self.service.sign_up(self.owner['name'], self.owner['password'])
        #self.assertNotEqual(result, False, 'add new owner failed')
        store = self.service.add_new_owner(self.store1['name'], self.owner['name'])
        self.assertNotEqual(store.success, False, 'add new owner failed')
        self.assertTrue({'username': self.owner['name']} in store.value['storeOwners'], 'add new owner failed')
        result = self.service.add_new_owner(self.store1['name'], self.owner['name']).success
        self.assertFalse(result, 'add new owner failed')

    def test_remove_owner(self):  # 4.4
        result = self.service.add_new_owner(self.store1['name'], self.owner['name'])
        self.assertTrue(result.success, 'add new owner failed')
        store = self.service.remove_owner(self.store1['name'], self.owner['name']) # based on add new owner
        self.assertTrue(store.success, 'remove owner failed')
        self.assertTrue({'username': self.owner['name']} not in [store.value['storeOwners']], 'remove owner failed')
        result = self.service.remove_owner(self.store1['name'], self.owner['name']).success
        self.assertFalse(result, 'remove owner failed')

    def test_add_new_manager(self):  # 4.5
        permissions = None#{'Edit': False, 'Remove': False, 'Add': True}
        store = self.service.add_new_manager(self.store1['name'], self.manager['name'], permissions)
        self.assertNotEqual(store.success, False, 'add new manager failed')
        self.assertTrue({'username': self.manager['name']} in store.value['storeManagers'], 'add new manager failed')
        self.service.remove_manager(self.store1['name'], self.manager['name'])

    def test_remove_manager(self):  # 4.6
        result = self.service.add_new_manager(self.store1['name'], self.manager['name'], None).success
        self.assertNotEqual(result, False, 'remove manager failed')
        store = self.service.remove_manager(self.store1['name'], self.manager['name'])
        self.assertNotEqual(store.success, False, 'add new manager failed')
        self.assertTrue({'username': self.manager['name']} not in store.value['storeManagers'], 'remove manager failed')


if __name__ == '__main__':
    unittest.main()
