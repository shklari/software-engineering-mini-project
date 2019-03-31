

# Interface
class Item(object):

    def __init__(self, name, price, policy=0):
        self.name = name
        self.price = price
        self.policy = policy

    def set_policy(self, new_policy): pass

    # 4.1.3
    def set_price(self, new_price): pass