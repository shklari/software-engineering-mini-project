# Interface
class SingletonCollectingSystem(object):

    def __init__(self):
        self.flagCollect = 1

    def switch(self):
        if self.flagCollect == 0:
            self.flagCollect = 1
        else:
            self.flagCollect = 0

    def init(self):
        if self.flagCollect == 0:
            return False
        else:
            return True

    def collect(self, amount, credit_details):
        def init(self):
            if self.flagCollect == 0:
                return 0
            else:
                return amount

    # 7
    # @staticmethod
    # def collect(amount, credit_details):
    #     if amount > credit_details.balance:
    #         return False
    #     return True


# Interface
class SingletonSupplyingSystem(object):

    def __init__(self):
        self.flagSupply = 1

    def switch(self):
        if self.flagSupply == 0:
            self.flagSupply = 1
        else:
            self.flagSupply = 0

    def init(self):
        if self.flagSupply == 0:
            return False
        else:
            return True

    def get_supply(self, item):
        return self.init()

    # 8
    # @staticmethod
    # def get_supply(user, items):
    #    return True


# Interface
class SingletonTraceabilitySystem(object):

    def __init__(self):
        self.flagTrace = 1

    def switch(self):
        if self.flagTrace == 0:
            self.flagTrace = 1
        else:
            self.flagTrace = 0

    def init(self):
        if self.flagTrace == 0:
            return False
        else:
            return True

    def trace(self, item, store):
        return self.init()


class CollectingSystem(object):

    instance = False

    def __init__(self):
        if not CollectingSystem.instance:
            CollectingSystem.instance = SingletonCollectingSystem()

    def init(self):
        return CollectingSystem.instance.init()

    def switch(self):
        return CollectingSystem.instance.switch()

    def collect(self, amount, credit_details):
        return CollectingSystem.instance.collect(amount, credit_details)


class SupplyingSystem(object):
    instance = False

    def __init__(self):
        if not SupplyingSystem.instance:
            SupplyingSystem.instance = SingletonSupplyingSystem()

    def init(self):
        return SupplyingSystem.instance.init()

    def switch(self):
        return SupplyingSystem.instance.switch()

    def get_supply(self, item):
        return SupplyingSystem.instance.get_supply(item)


class TraceabilitySystem(object):
    instance = False

    def __init__(self):
        if not TraceabilitySystem.instance:
            TraceabilitySystem.instance = SingletonTraceabilitySystem()

    def init(self):
        return TraceabilitySystem.instance.init()

    def switch(self):
        return TraceabilitySystem.instance.switch()

    def trace(self, item, store):
        return TraceabilitySystem.instance.trace(item, store)

