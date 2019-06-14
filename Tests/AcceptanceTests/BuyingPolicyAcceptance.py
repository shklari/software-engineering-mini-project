import unittest

from Service.serviceBridge import ServiceImpl
from Domain.BuyingPolicy import *


class FailImmediatePC(ImmediateBuyingPolicy):

    def apply_policy(self, obj):
        return False


class TestUserBuyingPolicy(unittest.TestCase):

    service = ServiceImpl()
    store1 = None
    store2 = None
    manager = None
    item1 = None
    sys_manager = None
    owner = None
    items = []
    user = None
    system = None

    # def __init__(self):
    #     self.service.create_store()
    # # store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
    # user {'username'}
    def setUp(self):
        self.service.init("avabash", "123456", 21, "")
        self.service.sign_up("good", "good", 77, "Israel")
        self.service.sign_up("young", "young", 14, "Israel")
        self.service.sign_up("badcountry", "badcountry", 30, "bad")
        self.service.login("avabash", "123456")
        self.store1 = self.service.create_store("shaioz", "avabash")
        self.service.add_item_to_inventory({'name': 'item1', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 1, "avabash")
        self.service.add_item_to_inventory({'name': 'item2', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 5, "avabash")
        self.store1 = self.service.get_store("shaioz").value
        self.item1 = self.store1.search_item_by_name("item1")
        self.item2 = self.store1.search_item_by_name("item2")
        self.age_policy = AgeLimitationUserPolicy(18)
        self.country_policy = CountryLimitationUserPolicy("bad")
        self.service.logout("avabash")

    def test_age_policy_success(self):
        self.item1.set_buying_policy(self.age_policy)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item1", 1, "good").success)

    def test_age_policy_fail(self):
        self.item1.set_buying_policy(self.age_policy)
        self.service.login("young", "young")
        self.assertFalse(self.service.add_to_cart("shaioz", "item1", 1, "young").success)

    def test_country_policy_success(self):
        self.item1.set_buying_policy(self.country_policy)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item1", 1, "good").success)

    def test_country_policy_fail(self):
        self.item1.set_buying_policy(self.country_policy)
        self.service.login("badcountry", "badcountry")
        self.assertFalse(self.service.add_to_cart("shaioz", "item1", 1, "badcountry").success)


class TestStoreBuyingPolicy(unittest.TestCase):

    service = ServiceImpl()
    store1 = None
    store2 = None
    manager = None
    item1 = None
    sys_manager = None
    owner = None
    items = []
    user = None
    system = None

    # def __init__(self):
    #     self.service.create_store()
    # # store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
    # user {'username'}
    def setUp(self):
        self.service.init("avabash", "123456", 21, "")
        self.service.sign_up("good", "good", 77, "Israel")
        self.service.sign_up("young", "young", 14, "Israel")
        self.service.sign_up("badcountry", "badcountry", 30, "bad")
        self.service.login("avabash", "123456")
        self.store1 = self.service.create_store("shaioz", "avabash")
        self.store1 = self.service.get_store("shaioz").value
        self.service.add_item_to_inventory({'name': 'item1', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 1, "avabash")
        self.service.add_item_to_inventory({'name': 'item2', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 5, "avabash")
        self.item1 = self.store1.search_item_by_name("item1")
        self.item2 = self.store1.search_item_by_name("item2")
        self.min_item_policy = MinQuantityStorePolicy("shaioz", 2)
        self.max_item_policy_bad = MaxQuantityStorePolicy("shaioz", 1)
        self.max_item_policy_good = MaxQuantityStorePolicy("shaioz", 5)
        self.service.logout("avabash")

    def test_min_policy_success(self):
        self.store1.set_buying_policy(self.min_item_policy)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item2", 5, "good").success)

    def test_min_policy_fail(self):
        self.store1.set_buying_policy(self.min_item_policy)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item1", 1, "good").success)

    def test_max_policy_success(self):
        self.store1.set_buying_policy(self.max_item_policy_good)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item2", 5, "good").success)

    def test_max_policy_fail(self):
        self.store1.set_buying_policy(self.max_item_policy_bad)
        self.service.login("good", "good")
        self.assertFalse(self.service.add_to_cart("shaioz", "item2", 5, "good").success)


class TestItemBuyingPolicy(unittest.TestCase):

    service = ServiceImpl()
    store1 = None
    store2 = None
    manager = None
    item1 = None
    sys_manager = None
    owner = None
    items = []
    user = None
    system = None

    # def __init__(self):
    #     self.service.create_store()
    # # store {'name', 'rank', 'inventory': [], 'storeOwners': [], 'storeManagers': [], 'discountPolicy'}
    # user {'username'}
    def setUp(self):
        self.service.init("avabash", "123456", 21, "")
        self.service.sign_up("good", "good", 77, "Israel")
        self.service.sign_up("young", "young", 14, "Israel")
        self.service.sign_up("badcountry", "badcountry", 30, "bad")
        self.service.login("avabash", "123456")
        self.store1 = self.service.create_store("shaioz", "avabash")
        self.service.add_item_to_inventory({'name': 'item1', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 1, "avabash")
        self.service.add_item_to_inventory({'name': 'item2', 'price': 3000, 'rank': 5, 'category': 'Electrics'},
                                           "shaioz", 5, "avabash")
        self.store1 = self.service.get_store("shaioz")
        self.item1 = self.store1.value.search_item_by_name("item1")
        self.item2 = self.store1.value.search_item_by_name("item2")
        self.min_item_policy = MinQuantityItemPolicy("item1", 3)
        self.max_item_policy_bad = MaxQuantityItemPolicy("item2", 1)
        self.max_item_policy_good = MaxQuantityItemPolicy("item2", 5)
        self.service.logout("avabash")

    def test_min_policy_success(self):
        self.item1.set_buying_policy(self.min_item_policy)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item1", 3, "good").success)

    def test_min_policy_fail(self):
        self.item1.set_buying_policy(self.min_item_policy)
        self.service.login("good", "good")
        self.assertFalse(self.service.add_to_cart("shaioz", "item1", 1, "good").success)

    def test_max_policy_success(self):
        self.item2.set_buying_policy(self.max_item_policy_good)
        self.service.login("good", "good")
        self.assertTrue(self.service.add_to_cart("shaioz", "item2", 5, "good").success)

    def test_max_policy_fail(self):
        self.item2.set_buying_policy(self.max_item_policy_bad)
        self.service.login("good", "good")
        self.assertFalse(self.service.add_to_cart("shaioz", "item2", 5, "good").success)
