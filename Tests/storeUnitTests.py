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
        self.owner = {'name':'Joseph'}
        self.manager = {'name': 'mana', 'password': '123456'}
        self.store1 = {'name': 'EL', 'manager': {'name': 'val', 'password': 'val'}, 'inventory': [], 'owner': {'name': 'val'}, 'rank': 3}
        self.store2 = {'name': 'Fox', 'manager': {'name': 'val', 'password': 'val'}, 'inventory': [], 'owner': {'name': 'val'}, 'rank': 2}
        self.store1['manager'] = self.manager
        self.store1['owner'] = self.owner
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
        result = self.service.add_to_cart(self.user, self.store1, self.items[0])
        self.assertTrue(result, 'add to cart failed')
        result = self.service.add_to_cart(self.user, self.store1, {'name': 'undefined', 'price': 0, 'rand': 5, 'category': 'undefined'})
        self.assertTrue(result, 'add to cart failed')
        result = self.service.add_to_cart(self.user, self.store2, self.items[2])
        self.assertTrue(result, 'add to cart failed')

    def test_isupper(self):#2.7
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
