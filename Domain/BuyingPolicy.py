

class BuyingPolicy(object):

    def apply_policy(self, obj):
        pass

    def is_composite(self):
        pass

    def policy_type(self):
        return ""

    def add_policy(self, policy):
        pass

    def check_contr(self, policy):
        return True


class ImmediateBuyingPolicy(BuyingPolicy):

    def apply_policy(self, obj):
        return True

    def is_composite(self):
        return False


class CompositeBuyingPolicy(BuyingPolicy):

    def __init__(self):
        self.policies = []

    def add_policy(self, policy):
        for pol in self.policies:
            if not pol.check_contr(policy):
                return False
        self.policies.append(policy)
        return True

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

    def apply_policy(self, cart):
        return self.country != cart.user.country


class ItemPolicy(ImmediateBuyingPolicy):

    def policy_type(self):
        return "item"


class MinQuantityItemPolicy(ItemPolicy):

    def __init__(self, item, min):
        self.item = item
        self.quantity = min

    def apply_policy(self, cart):
        for item in cart.items_and_quantities:
            if self.item == item:
                return self.quantity <= cart.items_and_quantities[item]
        return True

    def check_contr(self, policy):
        return policy.check_contr(self)


class StorePolicy(ImmediateBuyingPolicy):

    def policy_type(self):
        return "store"


class MaxQuantityItemPolicy(StorePolicy):

    def __init__(self, item, max):
        self.item = item
        self.quantity = max

    def apply_policy(self, cart):
        for item in cart.items_and_quantities:
            if self.item == item:
                return self.quantity >= cart.items_and_quantities[item]
        return True

    def check_contr(self, policy):
        if isinstance(policy, MinQuantityItemPolicy):
            return self.quantity < policy.quantity
        return True


class MinQuantityStorePolicy(ImmediateBuyingPolicy):

    def __init__(self, store_name, min):
        self.store_name = store_name
        self.quantity = min

    def apply_policy(self, cart):
        if self.store_name == cart.store_name:
            acc = 0
            for item in cart.items_and_quantities:
                acc += cart.items_and_quantities[item]
                if self.quantity <= acc:
                    return True
            return self.quantity <= acc
        return False

    def check_contr(self, policy):
        return policy.check_contr(self)


class MaxQuantityStorePolicy(ImmediateBuyingPolicy):

    def __init__(self, store_name, max):
        self.store_name = store_name
        self.quantity = max

    def apply_policy(self, cart):
        if self.store_name == cart.store_name:
            acc = 0
            for item in cart.items_and_quantities:
                acc += cart.items_and_quantities[item]
                if self.quantity < acc:
                    return False
        return True

    def check_contr(self, policy):
        if isinstance(policy, MinQuantityItemPolicy):
            return self.quantity > policy.quantity
        return True
