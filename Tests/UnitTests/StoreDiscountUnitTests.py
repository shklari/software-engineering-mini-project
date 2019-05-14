import unittest
from Domain.Store import Store
from Domain.User import User
from Domain.Guest import Guest
from Domain.Discounts.ImmediateDiscount import *
from Domain.Discounts.ComposedDiscount import *


class StoreDiscountUnitTests(unittest.TestCase):
    store = None
    admin = None
    user = None
    guest = None
    item1 = None

    def setUp(self):
        self.admin = User('admin', '112233')
        self.admin.logged_in = True
        self.user = User('user', '111111')
        self.guest = Guest()
        self.store = Store('Puppies', self.admin)
        self.item1 = {'name': 'Balishag', 'price': 100, 'category': 'smoking'}

    def test_add_store_discount(self):
        discount = ImmediateDiscount(0.2, 2, True, "stam")
        self.assertTrue(self.store.add_store_discount(self.admin, discount).success)
        self.assertFalse(self.store.add_store_discount(self.user, discount).success)
        self.assertFalse(self.store.add_store_discount(self.guest, discount).success)
        discount2 = ImmediateDiscount(0.1, 1, False, "")
        self.assertTrue(self.store.add_store_discount(self.admin, discount2).success)
        self.assertFalse(self.store.discount.double)
        composed = ComposedDiscount(0.5, 2, True, "")
        self.assertTrue(self.store.add_store_discount(self.admin, composed).success)

    def test_add_discount_to_item(self):
        discount = ImmediateDiscount(0.2, 2, True, "stam")
        self.assertFalse(self.store.add_discount_to_item(self.admin, 'Balishag', discount).success)
        self.store.add_item_to_inventory(self.admin, self.item1, 30)
        self.assertFalse(self.store.add_discount_to_item(self.user, 'Balishag', discount).success)
        self.assertFalse(self.store.add_discount_to_item(self.guest, 'Balishag', discount).success)
        self.assertTrue(self.store.add_discount_to_item(self.admin, 'Balishag', discount).success)
        composed = ComposedDiscount(0.5, 1, True, "50% discount on all items!")
        self.assertTrue(self.store.add_discount_to_item(self.admin, 'Balishag', composed).success)

    def test_apply_store_discount(self):
        self.assertEqual(self.store.apply_store_discount())






