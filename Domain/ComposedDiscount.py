from Domain.Discount import Discount


class ComposedDiscount(Discount):

    def __init__(self, percent, time):
        super(ComposedDiscount, self).__init__(percent, time)
        self.discounts = []

    def add_discount(self, discount):
        self.discounts.append(discount)

    def remove_discount(self, discount):
        self.discounts.remove(discount)



