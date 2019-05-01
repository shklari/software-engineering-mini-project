import unittest
from Service.serviceBridge import ServiceBridge


class CollectingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True

    def collect(self):
        return self.init()


class SupplyingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True

    def get_supply(self):
        return self.init()


class IntegritySystem(object):

    def __init__(self):
        self.flag = 1

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True


class UserTestCase(unittest.TestCase):
    item = {}
    store = {}
    system = ServiceBridge()
    manager = {"bascket": 0, "name": "man", "password": "123456"}
    collecting = CollectingSystem()
    supplying = SupplyingSystem()
    integrity = IntegritySystem()

    def setUp(self) -> None:
        self.item = 0
        self.store = 0
        self.system = ServiceBridge()
        self.manager = {"bascket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.integrity = IntegritySystem()

    # 2.6
    # adding item for a cart
    def test_add_to_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        items = self.system.search("shaioz")
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # test
        self.assertEqual(True, self.system.add_to_cart(self.store['name'], items[0]['name'], 1))

    # 2.6
    # adding item for a cart
    def test_add_to_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # test
        # item2 doesnt exist in shaiozim baam
        self.assertEqual(False, self.system.add_to_cart(self.store['name'], item2['name'], 2))
        # avocadosh store doesnt exist
        self.assertEqual(False, self.system.add_to_cart("avocadosh", item2['name'], 4))

    # 2.7.1
    def test_get_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1))
        self.cart = self.system.get_cart("shaiozim baam")
        self.assertIsNot(False, self.cart)
        self.assertEqual(self.store['name'], self.cart['store_name'])
        self.assertIsNot(None, self.cart.items_and_quantities[self.item['name']])

    # 2.7.1
    def test_get_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.cart = self.system.get_cart("shaiozim baam")
        # cart doesnt exist
        self.assertEqual(False, self.cart)
        self.system.add_to_cart("shaiozim baam", "shaioz", 1)
        self.assertEqual(None, self.system.get_cart("inbarim baam"))

    # 2.7.2
    def test_remove_from_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store.name, 1)
        # test
        cart1 = self.system.get_cart("shaiozim baam")
        length1 = len(cart1.items)
        self.assertEqual(True, self.system.remove_from_cart("shaiozim baam", "shaioz"))
        cart2 = self.system.get_cart("shaiozim baam")
        length2 = len(cart2.items)
        self.assertEqual(length1 - 1, length2)

    # 2.7.2
    def test_remove_from_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store.name, 1)
        # test
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "shaioz"))
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1))
        cart1 = self.system.get_cart("shaiozim baam")
        length1 = len(cart1.items)
        self.system.remove_from_cart("shaiozim baam", "shaioz")
        # item doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "glasses o mashu"))
        # store doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("inbarim baam", "shaioz"))

    # 2.8
    def test_buy_item_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        self.collecting.switch()
        # should work
        self.assertEqual(True, self.system.buy_items([self.item]))

    # 2.8
    def test_buy_item_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        self.collecting.switch()
        # collecting system doesnt work properly
        self.assertEqual(False, self.system.buy_items([self.item]))
        self.collecting.switch()
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_items([item2]))
        # not available
        self.assertEqual(False, self.system.buy_items([self.item]))


if __name__ == '__main__':
    unittest.main()