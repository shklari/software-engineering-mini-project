

class BuyingPolicy(object):

    def apply_policy(self, obj):
        pass

    def is_composite(self):
        pass

    def policy_type(self):
        return ""

    def add_policy(self, policy):
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
        pass

    def remove_policy(self, policy):
        self.policies.remove(policy)

    def is_composite(self):
        return True


class AndCompositeBuyingPolicy(CompositeBuyingPolicy):

    def apply_policy(self, obj):
        for policy in self.policies:
            if not policy.apply_policy(obj):
                return False
        return True

    def add_policy(self, policy):
        self.policies.append(policy)


class OrCompositeBuyingPolicy(CompositeBuyingPolicy):

    def apply_policy(self, obj):
        for policy in self.policies:
            if policy.apply_policy():
                return True
        return False


class UserPolicy(ImmediateBuyingPolicy):

    def policy_type(self):
        return 'user'


class AgeLimitationUserPolicy(UserPolicy):

    def __init__(self, age):
        self.age = age

    def apply_policy(self, cart):
        return self.age <= cart.user.age


class CountryLimitationUserPolicy(UserPolicy):

    def __init__(self, country):
        self.country = country

    def apply_policy(self, user):
        return self.country != user.country


class ItemPolicy(ImmediateBuyingPolicy):

    def policy_type(self):
        return "item"


class MinQuantityItemPolicy(ItemPolicy):

    def __init__(self, item, min):
        self.item = item
        self.quantity = min

    def apply_policy(self, cart):
        for item in cart['cart']:
            if self.item == item['name']:
                return self.quantity <= item['quantity']
        return True


class MaxQuantityItemPolicy(ItemPolicy):

    def __init__(self, item, max):
        self.item = item
        self.quantity = max

    def apply_policy(self, cart):
        for item in cart['cart']:
            if self.item == item.name:
                return self.quantity >= item.quantity
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


