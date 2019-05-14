from Domain.Discounts.ImmediateDiscount import ImmediateDiscount


class ConditionalDiscount(ImmediateDiscount):

    def __init__(self, condition, percent, time, double, description):
        super(ImmediateDiscount, self).__init__(percent, time, double, description)
        self.condition = condition

