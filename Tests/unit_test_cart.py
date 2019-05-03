from unittest import TestCase
from Domain.Cart import Cart
from Domain.System import System
from Domain.Item import Item


class UnitTestCart(TestCase):
    def setUp(self):
        self.system = System()
        self.zara_cart = Cart('zara')
        self.shirt = {'name': "shirt", 'price': 3, 'category': "cloths"}

    def test_add_item_to_cart(self):
        self.system.init_system('shaioz', '1234')
        self.system.login('shaioz', '1234')
        zara = self.system.create_store('zara')
        self.assertTrue(zara.add_item_to_inventory(self.system.cur_user, self.shirt, 4))
        self.assertTrue(self.system.add_item_to_cart('shirt', 3))

    def test_get_item_if_available(self):
        self.assertTrue(True)

    def test_remove_item_from_cart(self):
        self.assertTrue(True)

    def test_get_store_name(self):
        self.assertTrue(True)