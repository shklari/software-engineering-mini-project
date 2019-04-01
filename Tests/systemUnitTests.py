import unittest
from django.test import TestCase
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


class AllTestCase(TestCase):

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
        self.assertEqual(False, self.system.sign_up("need to fail", ""))
        self.assertEqual(False, self.system.sign_up("", "need to fail"))
        self.assertEqual(True, self.system.sign_up("try1", "try123"))
        self.assertEqual(False, self.system.sign_up("try1", "try123"))
        self.assertEqual(True, self.system.sign_up("try2", "try123"))
        self.assertEqual(False, self.system.sign_up("try1", "try111"))

    # 2.3
    def test_login(self):
        self.assertEqual(False, self.system.login("need to fail", ""))
        self.assertEqual(False, self.system.login("", "need to fail"))
        self.assertEqual(False, self.system.login("try1", "try111"))
        self.assertEqual(True, self.system.login("try1", "try123"))
        self.assertEqual(False, self.system.login("try1", "try123"))
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
        self.system.add_to_cart(self.store, [self.item])










class TestStringMethods(unittest.TestCase):

    service = SystemInterface()

    def setUp(self):
        manager = {'name': 'mana', 'password': '123456'}
        manager["name"]

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

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
