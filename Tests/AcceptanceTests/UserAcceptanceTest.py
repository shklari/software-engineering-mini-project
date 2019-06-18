import unittest
from Service.serviceBridge import ServiceImpl

from Domain.BuyingPolicy import ImmediateBuyingPolicy


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

    def collect(self, amount, credit_details):
        if self.flag == 0:
            return 0
        else:
            return amount


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

    def get_supply(self, name):
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
    system = ServiceImpl()
    manager = {"basket": 0, "name": "man", "password": "123456"}
    collecting = CollectingSystem()
    supplying = SupplyingSystem()
    consistency = ConsistencySystem()

    def setUp(self) -> None:
        self.item = 0
        self.store = 0
        self.system = ServiceImpl()
        self.manager = {"basket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.consistency = ConsistencySystem()
        self.system.init(self.manager['name'], self.manager['password'], 21, "")
        self.system.sign_up("try1", "try123", 21, "")
        self.system.sign_up("try2", "try123", 21, "")

    # 2.3
    def test_login_success(self):
        # test
        # should work
        self.assertEqual(True, self.system.login("try1", "try123").success)

    # 2.3
    def test_login_fail(self):
        # test
        # empty password
        self.assertEqual(False, self.system.login("need to fail", "").success)
        # empty user name
        self.assertEqual(False, self.system.login("", "need to fail").success)
        # wrong password
        self.assertEqual(False, self.system.login("try1", "try111").success)

    # 2.6
    # adding item for a cart
    def test_add_to_cart_success(self):
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.store = self.system.get_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store.name, 1, "try1")
        items = self.system.search("shaioz").value
        # test
        self.assertEqual(True, self.system.add_to_cart(self.store.name, items[0]['name'], 1, "try1").success)

    # 2.6
    # adding item for a cart
    def test_add_to_cart_fail(self):
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # test
        # item2 doesnt exist in shaiozim baam
        self.assertEqual(False, self.system.add_to_cart(self.store['name'], item2['name'], 2, "try1").success)
        # avocadosh store doesnt exist
        self.assertEqual(False, self.system.add_to_cart("avocadosh", item2['name'], 4, "try1").success)

    # 2.7.1
    def test_get_cart_success(self):
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        # test
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1, "try1").success)
        self.cart = self.system.get_cart("shaiozim baam", "try1")
        self.assertIsNot(False, self.cart.success)
        self.assertEqual(self.store['name'], self.cart.value['store_name'])
        self.assertIsNot(None, self.cart.value['items_and_quantities'][self.item['name']])

    # 2.7.2
    def test_remove_from_cart_success(self):
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        # test
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1, "try1").success)
        cart1 = self.system.get_cart("shaiozim baam", "try1").value
        print(cart1)
        length1 = len(cart1['items_and_quantities'])
        self.assertEqual(True, self.system.remove_from_cart("shaiozim baam", "shaioz", "try1").success)
        cart2 = self.system.get_cart("shaiozim baam", "try1").value
        length2 = len(cart2['items_and_quantities'])
        self.assertEqual(length1 - 1, length2)

    # 2.7.2
    def test_remove_from_cart_fail(self):
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        print(self.store)
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        # test
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "shaioz", "try1").success)
        self.assertIsNot(False, self.system.add_to_cart("shaiozim baam", "shaioz", 1, "try1").success)
        self.system.remove_from_cart("shaiozim baam", "shaioz", "try1")
        # item doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "glasses o mashu", "try1").success)
        # store doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("inbarim baam", "shaioz", "try1").success)

    # 2.8
    def test_buy_item_success(self):
        # setUp
        # set up stub ext systems:
#        self.system.real.sys.collecting_system = self.collecting
#        self.system.real.sys.supplying_system = self.supplying
#        self.system.real.sys.traceability_system = self.consistency
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo", "store_name": "shaiozim baam"}
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.store = self.system.get_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        self.system.add_to_cart("shaiozim baam", "shaioz", 1, "try1")
        # test
#        if self.collecting.flag == 0:
#            self.collecting.switch()
#        if self.consistency.flag == 0:
#            self.consistency.switch()
#        if self.supplying.flag == 0:
#            self.supplying.switch()
        # should work
        self.assertEqual(True, self.system.buy_items([self.item], "try1").success)

    # 2.8
    def test_buy_item_fail(self):
        # setUp
        # set up stub ext systems:
        self.system.sys.collecting_system = self.collecting
        self.system.sys.supplying_system = self.supplying
        self.system.sys.traceability_system = self.consistency
        self.system.login("try1", "try123")
        self.store = self.system.create_store("shaiozim baam", "try1").value
        self.item = {"name": "shaioz", "price": 11, "category": "omo", "store_name": "shaiozim baam",
                     "buying_policy": ImmediateBuyingPolicy()}
        self.system.add_item_to_inventory(self.item, self.store['name'], 1, "try1")
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        # collecting system doesnt work properly
        ret = self.system.buy_items([self.item], "try1").success
        self.assertEqual(False, ret)
        self.collecting.switch()
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa", "store_name": "shaiozim baam",
                 "buying_policy": ImmediateBuyingPolicy()}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_items([item2], "try1").success)
        # not available
        self.assertEqual(False, self.system.buy_items([self.item], "try1").success)


if __name__ == '__main__':
    unittest.main()
