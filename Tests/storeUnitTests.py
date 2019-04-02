import unittest
from Service.serviceBridge import ServiceBridge


class TestStore(unittest.TestCase):

    service = ServiceBridge()
    store1 = None
    store2 = None
    manager = None
    owner = None
    items =[]
    user = None

    def setUp(self):
        self.owner = {'name': 'Joseph'}
        self.manager = {'name': 'Itay', 'password': '123456'}
        self.store1 = {'name': 'EL', 'manager': [], 'inventory': [], 'storeOwners': [], 'rank': 3}
        self.store2 = {'name': 'Fox', 'manager': [], 'inventory': [], 'storeOwners': [], 'rank': 2}
        self.store1['manager'] = [self.manager]
        self.store1['owner'] = [self.owner]
        item1 = {'name': 'iphone7', 'price': 3000, 'rank': 5, 'category': 'Electrics'}
        item2 = {'name': 'Tv', 'price': 2000, 'rank': 4, 'category': 'Electrics'}
        item3 = {'name': 'pillow', 'price': 50, 'rank': 1, 'category': 'Home'}
        self.store1['inventory'] = self.items
        self.items = [item1, item2, item3]
        self.user = {'basket': []}
        self.store2['manager'] = self.manager
        self.store2['owner'] = self.owner
        self.store2['inventory'] = [item1, item2]

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

    def test_addItemToInventory(self):# 4.1.1
        store = self.service.add_item_to_inventory(self.items[0], self.store1['name'], 2)
        self.assertTrue(self.items[0]['name'] in store['inventory'], 'add item to inventory failed')
        self.assertEqual(self.items[0]['quantity'], 2, 'add item to inventory failed')

    def test_removeItemFromInventory(self):  # 4.1.2
        store = self.service.remove_item_from_inventory(self.items[0]['name'], self.store1['name'], 2)
        self.assertFalse(self.items[0]['name'] in store['inventory'], 'remove item to inventory failed')
        result = self.service.remove_item_from_inventory(self.items[1]['name'], self.store1['name'], 2)
        self.assertFalse(result, 'remove item to inventory failed')

    def test_editItemFromInventory(self):  # 4.1.3
        self.service.add_item_to_inventory(self.items[0], self.store1, 2)
        item = self.service.edit_item_price(self.store1['name'], self.items[0]['name'], 100)
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')

    def test_add_new_owner(self):  # 4.3 Todo: finish
        self.service.add_new_owner(self.manager['name'])
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')
        self.service.add_new_owner(self.owner['name'])
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')

    def test_remove_new_owner(self):  # 4.4 Todo: finish
        self.service.remove_owner(self.owner['name'])
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')

    def test_add_new_manager(self):  # 4.5 Todo: finish
        self.service.add_new_manager(self.owner['name'])
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')
        self.service.add_new_manager(self.user['name'])
        self.assertTrue(item['price'], 100, 'edit item from inventory failed')

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
