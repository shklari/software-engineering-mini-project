from abc import abstractmethod


class Discount(object):

    # description is a string describing the discount that is displayed to the user
    def __init__(self, percent, time, double, description):
        self.percent = percent
        self.time = time
        self.double = double
        self.description = description

    @abstractmethod
    def apply_discount(self, price): pass

