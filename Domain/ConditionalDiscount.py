from Domain.ImmediateDiscount import ImmediateDiscount


class ConditionalDiscount(ImmediateDiscount):

    def __init__(self, condition):
        self.condition = condition

