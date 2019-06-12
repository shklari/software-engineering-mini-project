import unittest
from Domain.Basket import Basket
from Domain.Cart import Cart
from Domain.Store import Store
from Domain.User import User


class StoreUnitTests(unittest.TestCase):

    basket = None
    cart = None
    store = None
    user = None

    def setUp(self):
        self.user = User('the oz', '112233', 21, "")
        self.user.logged_in = True
        self.store = Store("shklar\'s", self.user)
        self.basket = Basket()
        self.cart = Cart("shklar\'s")

    def test_add_cart(self):
        self.basket.add_cart(self.cart)
        self.assertTrue(len(self.basket.carts) == 1)
        self.assertTrue(self.cart in self.basket.carts)

    def test_remove_item_from_cart(self):
        self.cart.add_item_to_cart('bamba', 2)
        self.basket.add_cart(self.cart)
        self.assertEqual(len(self.basket.carts), 1)
        self.assertTrue(self.cart in self.basket.carts)
        self.basket.remove_item_from_cart(self.store.name, 'bamba')
        self.assertFalse(self.cart.get_item_if_available('bamba'))

