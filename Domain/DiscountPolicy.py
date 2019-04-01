

# interface
class DiscountPolicy(object):
    def __init__(self, discount):
        self.discount = discount

    def apply_discount(self, amount):
        return (1 - self.discount) * amount