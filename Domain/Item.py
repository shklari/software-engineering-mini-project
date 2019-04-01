from .ProcurementPolicy import ProcurementPolicy


# Interface
class Item(object):

    def __init__(self, name, price, category, rank):
        self.name = name
        self.price = price
        self.category = category
        self.rank = rank
        self.procPolicy = 0;

    def set_policy(self, new_policy):
        if isinstance(new_policy, ProcurementPolicy):
            self.procPolicy = new_policy;
            print("new policy has updated")
            return True
        print("illegal policy")
        return False

    # 4.1.3
    def set_price(self, new_price):
        self.price = new_price
