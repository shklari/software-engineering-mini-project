from Domain.Discounts.ComposedDiscount import *
from Domain.BuyingPolicy import ImmediateBuyingPolicy


# Interface
class Item(object):

    def __init__(self, name, price, category, store_name):
        self.name = name
        self.price = price
        self.category = category
        self.rank = 0
        self.store_name = store_name
        self.discount = ComposedDiscount(0, 0, True, "")
        self.buying_policy = ImmediateBuyingPolicy()

    # 4.1.3
    def set_price(self, new_price):
        self.price = new_price

    def set_rank(self, new_rank):
        self.rank = new_rank

    # new_discount is a Discount object
    def add_discount(self, new_discount):
        self.discount.add_discount(new_discount)

    def add_policy(self, policy_name, val):
        self.buying_policy.add_policy(policy_name)

    def apply_discount(self):
        return self.discount.apply_discount(self.price)

    def set_buying_policy(self, policy):
        self.buying_policy = policy

    def add_buying_policy(self, policy):
        if self.buying_policy.is_composite():
            self.buying_policy.add_policy(policy)
        else:
            comp = CompositeBuyingPolicy()
            comp.add_policy(self.buying_policy)
            comp.add_policy(policy)
            self.buying_policy = comp

    def remove_buying_policy(self, policy):
        if self.buying_policy == policy:
            self.buying_policy = ImmediateBuyingPolicy()
        elif self.buying_policy.is_composite():
            self.buying_policy.remove_policy(policy)




