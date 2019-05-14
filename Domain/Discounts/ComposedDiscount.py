from Domain.Discounts.Discount import Discount


class ComposedDiscount(Discount):

    def __init__(self, percent, time, double, description):
        super(ComposedDiscount, self).__init__(percent, time, double, description)
        self.discounts = []

    def add_discount(self, discount):
        self.discounts.append(discount)

    def remove_discount(self, discount):
        self.discounts.remove(discount)

    def apply_discount(self, price):
        new_price = price
        if self.time > 0:
            new_price = new_price * (1 - self.percent)
        else:
            self.double = True
        if self.double:
            for d in self.discounts:
                new_price = d.apply_discount(new_price)
                if not d.double:
                    return new_price
        return new_price

    def set_discount_time(self, time):
        self.time = time




