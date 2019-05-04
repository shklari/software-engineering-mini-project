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


class SystemTestCase(unittest.TestCase):
    item = {}
    store = {}
    system = ServiceBridge()
    manager = {"bascket": 0, "name": "man", "password": "123456"}
    collecting = CollectingSystem()
    supplying = SupplyingSystem()
    consistency = ConsistencySystem()

    def setUp(self) -> None:
        self.item = 0
        self.store = 0
        self.system = ServiceBridge()
        self.manager = {"bascket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.consistency = ConsistencySystem()

    # 1.1 # init will succeed only if the external systems.init() will return true
    def test_init(self):
        self.collecting.switch()
        self.supplying.switch()
        self.consistency.switch()
        for i in range(0, 1):
            for j in range(0, 1):
                for k in range(0, 1):
                    inits = self.system.init(self.manager['name'], self.manager['password']).success
                    self.assertEqual((i == 1 and j == 1 and k == 1), inits)
                    self.collecting.switch()
                self.supplying.switch()
            self.consistency.switch()
        self.collecting.switch()
        self.supplying.switch()
        self.consistency.switch()

    # 2.2
    def test_signup_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        # test
        # should work
        self.assertEqual(True, (self.system.sign_up("try1", "try123")).success)
        # already exists
        self.system.sign_up("try1", "try123")
        # should work
        self.assertEqual(True, (self.system.sign_up("try2", "try123")).success)

    # 2.2
    def test_signup_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        # test
        # empty password
        self.assertEqual(False, (self.system.sign_up("need to fail", "")).success)
        # empty user name
        self.assertEqual(False, (self.system.sign_up("", "need to fail")).success)
        # should work
        self.system.sign_up("try1", "try123")
        # already exists
        self.assertEqual(False, (self.system.sign_up("try1", "try123")).success)
        # should work
        self.system.sign_up("try2", "try123")
        # already exists
        self.assertEqual(False, (self.system.sign_up("try1", "try111")).success)

    # 2.5
    def test_search_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam")
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertEqual(self.system.search("shaioz").value[0]['category'], "omo")
        self.assertEqual(self.system.search("omo").value[0]['name'], "shaioz")

    # 2.5
    def test_search_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        self.assertEqual(self.system.search("avabash").value, [])

    # 3.1
    def test_logout_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # user isn't logged in - shouldnt work
        self.system.login("try1", "try123")
        # user is logged in - should work
        self.assertEqual(True, self.system.logout().success)
        self.assertEqual(False, self.system.real.sys.cur_user.logged_in)

    # 3.1
    def test_logout_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        # user isn't logged in - shouldnt work
        self.assertEqual(False, self.system.logout().success)
        self.system.login("try1", "try123")
        # user is logged in - should work
        self.system.logout()
        # user is already logged out - shouldnt work
        self.assertEqual(False, self.system.logout().success)

    # 6.2
    def test_remove_user_success(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login(self.manager['name'], self.manager['password'])
        # test
        self.system.login("man", "123456")
        # should work
        self.assertEqual(True, self.system.remove_user("try2").success)
        for user in self.system.real.sys.users:
            self.assertNotEqual("try2", user)

    # 6.2
    def test_remove_user_fail(self):
        # setUp
        self.system.init(self.manager['name'], self.manager['password'])
        self.system.sign_up("try1", "try123")
        self.system.sign_up("try2", "try123")
        self.system.login(self.manager['name'], self.manager['password'])
        # test
        # cant remove the system manager
        self.assertEqual(False, self.system.remove_user("man").success)
        self.system.login("man", "123456")
        # doesnt exist
        self.assertEqual(False, self.system.remove_user("try3").success)
        self.system.remove_user("try2")
        # doesn't exist
        self.assertEqual(False, self.system.remove_user("try2").success)


if __name__ == '__main__':
    unittest.main()
