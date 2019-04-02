import unittest
from Domain.Basket import Basket
from Domain.Cart import Cart


class StoreUnitTests(unittest.TestCase):

    basket = None
    cart = None

    def setUp(self):
        self.basket = Basket()
        self.cart = Cart("Puppies better")

    def test_add_cart(self):
        self.basket.add_cart(self.cart)
        self.assertTrue(len(self.basket.carts) == 1)
        self.assertTrue(self.cart in self.basket.carts)