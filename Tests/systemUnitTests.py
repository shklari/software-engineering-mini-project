import unittest
from Service.serviceBridge import ServiceBridge
# from Service.service import ServiceInterface

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


class SystemTestCase(unittest.TestCase):
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

    # 1.1 # init will succeed only if the external systems.init() will return true
    def test_init(self):
        self.collecting.switch()
        self.supplying.switch()
        self.integrity.switch()
        for i in range(0, 1):
            for j in range(0, 1):
                for k in range(0, 1):
                    inits = self.system.init(self.manager['name'], self.manager['password'])
                    self.assertEqual((i == 1 and j == 1 and k == 1), inits)
                    self.collecting.switch()
                self.supplying.switch()
            self.integrity.switch()
        self.collecting.switch()
        self.supplying.switch()
        self.integrity.switch()

    # 2.2
    def test_signup(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        # test
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
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # test
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
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertEqual(self.system.search("shaioz")[0]['category'], "omo")
        self.assertEqual(self.system.search("omo")[0].name, "shaioz")
        self.assertEqual(self.system.search("avabash"), [])

    # 2.6
    def test_add_to_cart(self):
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
        # item2 doesnt exist in shaiozim baam
        self.assertEqual(False, self.system.add_to_cart(self.store['name'], item2['name'], 2))
        # avocadosh store doesnt exist
        self.assertEqual(False, self.system.add_to_cart("avocadosh", item2['name'], 4))

    # 2.7.1
    def test_get_cart(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store.name, 1)
        self.cart = self.system.get_cart("shaiozim baam")
        # test
        self.assertEqual(self.store['name'], self.cart.store_name)
        self.assertIsNot(None, self.cart.items_and_quantities[self.item['name']])
        self.assertEqual(None, self.system.get_cart("inbarim baam"))

    # 2.7.2
    def test_remove_from_cart(self):
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
        # item doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("shaiozim baam", "glasses o mashu"))
        # store doesnt exist
        self.assertEqual(False, self.system.remove_from_cart("inbarim baam", "shaioz"))

    # 2.8
    def test_buy_item(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store.name, 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        self.collecting.switch()
        # collecting system doesnt work properly
        self.assertEqual(False, self.system.buy_item(self.item))
        self.collecting.switch()
        # should work
        self.assertEqual(True, self.system.buy_item(self.item))
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa"}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_item(item2))
        # not available
        self.assertEqual(False, self.system.buy_item(self.item))

    # 3.1
    def test_logout(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # user isn't logged in - shouldnt work
        self.assertEqual(False, self.system.logout())
        self.system.login("try1", "try123")
        # user is logged in - should work
        self.assertEqual(True, self.system.logout())
        # user is already logged out - shouldnt work
        self.assertEqual(False, self.system.logout())

    # 6.2
    def test_remove_user(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login(self.manager['name'], self.manager['password'])
        # test
        # cant remove the system manager
        self.assertEqual(False, self.system.remove_user("man"))
        self.system.login("man", "123456")
        # doesnt exist
        self.assertEqual(False, self.system.remove_user("try3"))
        # should work
        self.assertEqual(True, self.system.remove_user("try2"))
        # doesn't exist
        self.assertEqual(False, self.system.remove_user("try2"))


if __name__ == '__main__':
    unittest.main()
