# Interface
class CollectingSystem(object):

    def init(self): pass

    # 7
    def collect(self, amount, credit_details): pass


# Interface
class SupplyingSystem(object):

    def init(self): pass

    # 8
    def get_supply(self, user, items): pass