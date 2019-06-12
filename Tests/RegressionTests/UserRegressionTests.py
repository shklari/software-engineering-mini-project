import unittest
from Service.serviceBridge import ServiceImpl


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


    # 2.8
    def test_buy_item_success(self):
        # setUp
        # set up stub ext systems:
        self.system.real.sys.collecting_system = self.collecting
        self.system.real.sys.supplying_system = self.supplying
        self.system.real.sys.traceability_system = self.consistency
        self.system.init(self.manager['name'], self.manager['password'], 21, "")
        self.system.sign_up("try1", "try123", 21, "")
        self.system.sign_up("try2", "try123", 21, "")
        self.system.login("try1", "try123")
        self.item = {"name": "shaioz", "price": 11, "category": "omo", "store_name": "shaiozim baam"}
        self.store = self.system.create_store("shaiozim baam").value
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        self.system.add_to_cart("shaiozim baam", "shaioz", 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        if self.consistency.flag == 0:
            self.consistency.switch()
        if self.supplying.flag == 0:
            self.supplying.switch()
        # should work
        self.assertEqual(True, self.system.buy_items([self.item]).success)


    # 2.8
    def test_buy_item_fail(self):
        # setUp
        # set up stub ext systems:
        self.system.real.sys.collecting_system = self.collecting
        self.system.real.sys.supplying_system = self.supplying
        self.system.real.sys.traceability_system = self.consistency
        self.system.init(self.manager['name'], self.manager['password'], 21, "")
        self.system.sign_up("try1", "try123", 21, "")
        self.system.sign_up("try2", "try123", 21, "")
        self.system.login("try1", "try123")
        self.store = self.system.create_store("shaiozim baam").value
        self.item = {"name": "shaioz", "price": 11, "category": "omo", "store_name": "shaiozim baam"}
        self.system.add_item_to_inventory(self.item, self.store['name'], 1)
        # test
        if self.collecting.flag == 0:
            self.collecting.switch()
        # collecting system doesnt work properly
        ret = self.system.buy_items([self.item]).success
        self.assertEqual(False, ret)
        self.collecting.switch()
        item2 = {"name": "avabash", "price": 18, "category": "mefakedet girsa", "store_name": "shaiozim baam"}
        # item doesnt exist
        self.assertEqual(False, self.system.buy_items([item2]).success)
        # not available
        self.assertEqual(False, self.system.buy_items([self.item]).success)
