import unittest
from django.test import TestCase
from Service.serviceBridge import ServiceBridge

# ############################ must run all in order

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


class SystemTestCase(TestCase):

    def __init__(self):
        super()

    def setUp(self) -> None:
        self.item = 0
        self.store = 0
        self.system = ServiceBridge()
        self.manager = {"bascket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.integrity = IntegritySystem()

    # 1.1 # init will succeed only if the external systems.init() will return true
    def test_init(self):
        for i in range(0, 1):
            for j in range(0, 1):
                for k in range(0, 1):
                    self.assertEqual((i == 1 and j == 1 and k == 1), self.system.init(self.manager, self.collecting, self.supplying, self.integrity))
                    self.collecting.switch()
                self.supplying.switch()
            self.integrity.switch()

    # 2.2
    def test_signup(self):
        # empty password
        self.assertEqual(False, self.system.sign_up("need to fail", ""))
        # empty user name
        self.assertEqual(False, self.system.sign_up("", "need to fail"))
        # should work
        self.assertEqual(True, self.system.sign_up("try1", "try123"))
        # already exists
        self.assertEqual(False, self.system.sign_up("try1", "try123"))
        # should work
        self.assertEqual(True, self.system.sign_up("try2", "try123"))
        # already exists
        self.assertEqual(False, self.system.sign_up("try1", "try111"))

    # 2.3
    def test_login(self):
        # empty password
        self.assertEqual(False, self.system.login("need to fail", ""))
        # empty user name
        self.assertEqual(False, self.system.login("", "need to fail"))
        # wrong password
        self.assertEqual(False, self.system.login("try1", "try111"))
        # should work
        self.assertEqual(True, self.system.login("try1", "try123"))
        # already logged in
        self.assertEqual(False, self.system.login("try1", "try123"))
        # already logged in
        self.assertEqual(False, self.system.login("try2", "try123"))

    # 2.5
    def test_search(self):
        self.item = {"name": "shaioz", "price": 11, "category": "omo", "rank": 4}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.store, self.item, 1)
        self.assertEqual(self.system.search("shaioz")[0].category, "omo")
        self.assertEqual(self.system.search("omo")[0].name, "shaioz")
        self.assertEqual(self.system.search("avabash"), [])

    # 2.6
    def test_add_to_cart(self):
        items = self.system.search("shaioz")
        self.assertEqual(True, self.system.add_to_cart(self.store.name, items[0]))
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa", "rank": 5}
        # item2 doesnt exist in shaiozim baam
        self.assertEqual(False, self.system.add_to_cart(self.store.name, item2))
        # avocadosh store doesnt exist
        self.assertEqual(False, self.system.add_to_cart("avocadosh", item2))

    # 2.7.1
    def test_get_cart(self):
        self.cart = self.system.get_cart("shaiozim baam")
        self.assertEqual(self.store.name, self.cart.storeName)
        self.assertEqual(self.item, self.cart.items[0])
        self.assertEqual(None, self.system.get_cart("inbarim baam"))

    # 2.7.2
    def test_remove_from_cart(self):
        cart1 = self.system.get_cart("shaiozim baam")
        item = cart1.items[0]
        length1 = len(cart1.items)
        self.assertEqual(True, self.system.remove_from_cart("shaiozim baam", item))
        cart2 = self.system.get_cart("shaiozim baam")
        length2 = len(cart2.items)
        self.assertEqual(length1 - 1, length2)
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "glasses o mashu"))
        self.assertEqual(False, self.system.remove_from_cart("inbarim baam", "glasses o mashu"))

    # 2.8
    def test_buy_item(self):
        if(self.collecting.flag == 0):
            self.collecting.switch()
        self.collecting.switch()
        # collecting system doesnt work properly
        self.assertEqual(False, self.system.buy_item(self.item))
        self.collecting.switch()
        # should work
        self.assertEqual(True, self.system.buy_item(self.item))
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa", "rank": 5}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_item(item2))
        # not available
        self.assertEqual(False, self.system.buy_item(self.item))

    # 3.1
    def test_logout(self):
        # user is logged in - should work
        self.assertEqual(True, self.system.logout())
        # user is loged out - shouldnt work
        self.assertEqual(False, self.system.logout())

    # 6.2
    def test_remove_client(self):
        self.assertEqual(False, self.system.remove_client("man"))
        self.system.login("man", "123456")
        # doesnt exist
        self.assertEqual(False, self.system.remove_client("try3"))
        # should work
        self.assertEqual(True, self.system.remove_client("try2"))
        # doesn't exist
        self.assertEqual(False, self.system.remove_client("try2"))


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.manager = 'FOO'

    def test_upper(self):
        self.assertEqual('foo'.upper(), self.manager)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
