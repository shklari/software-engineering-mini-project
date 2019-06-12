

class BuyingPolicy(object):

    def apply_policy(self, obj):
        pass

    def is_composite(self):
        pass


class ImmediateBuyingPolicy(BuyingPolicy):

    def apply_policy(self, obj):
        return True

    def is_composite(self):
        return False


class CompositeBuyingPolicy(BuyingPolicy):

    def __init__(self):
        self.policies = []

    def add_policy(self, policy):
        self.policies.append(policy)

    def remove_policy(self, policy):
        self.policies.remove(policy)

    def is_composite(self):
        return True


class MinQuantityItemPolicy(ImmediateBuyingPolicy):

    def __init__(self, item, min):
        self.item = item
        self.quantity = min

    def apply_policy(self, cart):
        for item in cart['cart']:
            if self.item == item['name']:
                return self.quantity <= item['quantity']
        return True


class MaxQuantityItemPolicy(ImmediateBuyingPolicy):

    def __init__(self, item, max):
        self.item = item
        self.quantity = max

    def apply_policy(self, cart):
        for item in cart['cart']:
            if self.item == item['name']:
                return self.quantity >= item['quantity']
        return True


class MaxQuantityStorePolicy(ImmediateBuyingPolicy):

    def __init__(self, store_name, max):
        self.store_name = store_name
        self.quantity = max

    def apply_policy(self, cart):
        if self.store_name == cart['store']:
            acc = 0
            for item in cart['cart']:
                acc += item.quantity
                if self.quantity < acc:
                    return False
        return True


class MinQuantityStorePolicy(ImmediateBuyingPolicy):

    def __init__(self, store_name, min):
        self.store_name = store_name
        self.quantity = min

    def apply_policy(self, cart):
        if self.store_name == cart['store']:
            acc = 0
            for item in cart['cart']:
                if self.quantity < acc:
                    acc += item.quantity
                else:
                    return True
            return False
        return True


class AndCompositeBuyingPolicy(CompositeBuyingPolicy):

    def apply_policy(self, obj):
        for policy in self.policies:
            if not policy.apply_policy(obj):
                return False
        return True


class OrCompositeBuyingPolicy(CompositeBuyingPolicy):

    def apply_policy(self, obj):
        for policy in self.policies:
            if policy.apply_policy():
                return True
        return False

    def add_policy(self, policy):
        self.policies.append(policy)

    def remove_policy(self, policy):
        self.policies.remove(policy)

    def is_composite(self):
        return True


class AgeLimitationUserPolicy(ImmediateBuyingPolicy):

    def __init__(self, age):
        self.age = age

    def apply_policy(self, user):
        return True if (self.age <= user.age) else False


class CountryLimitationUserPolicy(ImmediateBuyingPolicy):

    def __init__(self, country):
        self.country = country

    def apply_policy(self, user):
        return True if (self.country <= user.country) else False

