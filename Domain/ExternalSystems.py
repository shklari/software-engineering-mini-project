# Interface
class CollectingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True

    def collect(self, amount, credit_details):
        return self.init()

    # 7
    # @staticmethod
    # def collect(amount, credit_details):
    #     if amount > credit_details.balance:
    #         return False
    #     return True


# Interface
class SupplyingSystem(object):

    def __init__(self):
        self.flag = 0

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True

    def get_supply(self):
        return self.init()

    # 8
    # @staticmethod
    # def get_supply(user, items):
    #    return True


# Interface
class TraceabilitySystem(object):

    def __init__(self):
        self.flag = 1

    def switch(self):
        if self.flag == 0:
            self.flag = 1
        else:
            self.flag = 0

    def init(self):
        if self.flag == 0:
            return False
        else:
            return True

    def trace(self, item, store):
        return self.init()

