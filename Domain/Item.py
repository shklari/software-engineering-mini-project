from Domain.Discounts.ComposedDiscount import *


# Interface
class Item(object):

    def __init__(self, name, price, category, store_name):
        self.name = name
        self.price = price
        self.category = category
        self.rank = 0
        self.store_name = store_name
        self.discount = ComposedDiscount(0, 0, True, "")

    # 4.1.3
    def set_price(self, new_price):
        self.price = new_price

    def set_rank(self, new_rank):
        self.rank = new_rank

    # new_discount is a Discount object
    def add_discount(self, new_discount):
        self.discount.add_discount(new_discount)

    def apply_discount(self):
        return self.discount.apply_discount(self.price)


