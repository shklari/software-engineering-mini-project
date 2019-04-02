from .ProcurementPolicy import ProcurementPolicy


# Interface
class Item(object):

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        self.rank = 0

    # 4.1.3
    def set_price(self, new_price):
        self.price = new_price
