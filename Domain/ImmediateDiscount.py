from Domain.Discount import Discount


class ImmediateDiscount(Discount):

    def __init__(self, percent, time):
        super(ImmediateDiscount, self).__init__(percent, time)


