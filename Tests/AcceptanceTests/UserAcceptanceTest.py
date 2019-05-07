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


class ConsistencySystem(object):

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
    manager = {"basket": 0, "name": "man", "password": "123456"}
    collecting = CollectingSystem()
    supplying = SupplyingSystem()
    consistency = ConsistencySystem()

    def setUp(self) -> None:
        self.item = 0
        self.store = 0
        self.system = ServiceBridge()
        self.manager = {"basket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.consistency = ConsistencySystem()

    # 2.3
    def test_login_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # test
        # should work
        self.assertEqual(True, self.system.login("try1", "try123").success)
        self.assertEqual("try1", self.system.real.sys.cur_user.username)
        # already logged in
        self.system.login("try2", "try123")
        self.assertEqual("try1", self.system.real.sys.cur_user.username)

    # 2.3
    def test_login_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # test
        # empty password
        self.assertEqual(False, self.system.login("need to fail", "").success)
        # empty user name
        self.assertEqual(False, self.system.login("", "need to fail").success)
        # wrong password
        self.assertEqual(False, self.system.login("try1", "try111").success)
        # should work
        self.system.login("try1", "try123")
        # already logged in
        self.assertEqual(False, self.system.login("try1", "try123").success)
        # already logged in
        self.assertEqual(False, self.system.login("try2", "try123").success)
        self.assertEqual("try1", self.system.real.sys.cur_user.username)

    # 2.6
    # adding item for a cart
    def test_add_to_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        items = self.system.search("shaioz").value
        # test
        self.assertEqual(True, self.system.add_to_cart(self.store['name'], items[0]['name'], 1).success)

    # 2.6
    # adding item for a cart
    def test_add_to_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # test
        # item2 doesnt exist in shaiozim baam
        self.assertEqual(False, self.system.add_to_cart(self.store['name'], item2['name'], 2).success)
        # avocadosh store doesnt exist
        self.assertEqual(False, self.system.add_to_cart("avocadosh", item2['name'], 4).success)

    # 2.7.1
    def test_get_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1).success)
        self.cart = self.system.get_cart("shaiozim baam")
        self.assertIsNot(False, self.cart.success)
        self.assertEqual(self.store['name'], self.cart.value['store_name'])
        self.assertIsNot(None, self.cart.value['items_and_quantities'][self.item['name']])

    # 2.7.1
    def test_get_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.cart = self.system.get_cart("shaiozim baam").value
        # cart doesnt exist
        self.assertEqual(None, self.cart)
        self.system.add_to_cart("shaiozim baam", "shaioz", 1)
        self.assertEqual(None, self.system.get_cart("inbarim baam").value)

    # 2.7.2
    def test_remove_from_cart_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1).success)
        cart1 = self.system.get_cart("shaiozim baam").value
        print(cart1)
        length1 = len(cart1['items_and_quantities'])
        self.assertEqual(True, self.system.remove_from_cart("shaiozim baam", "shaioz").success)
        cart2 = self.system.get_cart("shaiozim baam").value
        length2 = len(cart2['items_and_quantities'])
        self.assertEqual(length1 - 1, length2)

    # 2.7.2
    def test_remove_from_cart_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        print(self.store)
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "shaioz").success)
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1).success)
        self.system.remove_from_cart("shaiozim baam", "shaioz")
        # item doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "glasses o mashu").success)
        # store doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("inbarim baam", "shaioz").success)

    # 2.8
    def test_buy_item_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        self.collecting.switch()
        # should work
        self.assertEqual(True, self.system.buy_items([self.item]).success)

    # 2.8
    def test_buy_item_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        self.collecting.switch()
        # collecting system doesnt work properly
        self.assertEqual(False, self.system.buy_items([self.item]).success)
        self.collecting.switch()
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_items([item2]).success)
        # not available
        self.assertEqual(False, self.system.buy_items([self.item]).success)


if __name__ == '__main__':
    unittest.main()
