# Interface
class CollectingSystem(object):

    # 7
    @staticmethod
    def collect(amount, credit_details):
        if amount > credit_details.balance:
            return False
        return True


# Interface
class SupplyingSystem(object):

    # 8
    @staticmethod
    def get_supply(user, items):
        return True


# Interface
class TraceabilitySystem(object):

    def trace(self, item, store): pass
