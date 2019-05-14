import unittest
from Domain.Item import Item
from Domain.Store import Store
from Domain.User import User
from Domain.Guest import Guest
from Domain.Discounts.ImmediateDiscount import *
from Domain.Discounts.ComposedDiscount import *


class ItemDiscountUnitTests(unittest.TestCase):

    item = None

    def setUp(self):
        self.item = Item('iRobot', 500, 'home appliance', 'Home Robots')

    def test_item_discount(self):
        self.assertTrue(isinstance(self.item.discount, ComposedDiscount))
        self.assertEqual(self.item.discount.percent, 0)

    def test_apply_discount(self):
        self.assertEqual(self.item.apply_discount(), 500)
        zero_discount = ImmediateDiscount(0.7, 0, True, "")
        self.item.add_discount(zero_discount)
        self.assertEqual(self.item.apply_discount(), 500)
        zero_discount.set_discount_time(1)
        self.assertEqual(int(self.item.apply_discount()), 150)

    def test_add_discount(self):
        discount = ImmediateDiscount(0.5, 2, True, "50% on iRobots!")
        self.item.add_discount(discount)
        new_price = self.item.apply_discount()
        self.assertEqual(int(new_price), 250)
        discount2 = ImmediateDiscount(0.1, 1, True, "10%")
        self.item.add_discount(discount2)
        new_price = self.item.apply_discount()
        self.assertEqual(int(new_price), 225)

