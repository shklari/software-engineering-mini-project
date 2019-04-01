from .ProcurementPolicy import ProcurementPolicy


# Interface
class Item(object):

    def __init__(self, name, price, category, rank):
        self.name = name
        self.price = price
        self.category = category
        self.rank = rank

    # 4.1.3
    def set_price(self, new_price):
        self.price = new_price
