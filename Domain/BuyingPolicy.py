

class BuyingPolicy(object):

    def apply_policy(self):
        pass

    def is_composite(self):
        pass


class ImmediateBuyingPolicy(BuyingPolicy):

    def apply_policy(self):
        return True

    def is_composite(self):
        return False


class CompositeBuyingPolicy(BuyingPolicy):

    def __init__(self):
        self.policies = []

    def apply_policy(self):
        for policy in self.policies:
            if not policy.apply_policy():
                return False
        return True

    def add_policy(self, policy):
        self.policies.append(policy)

    def remove_policy(self, policy):
        self.policies.remove(policy)

    def is_composite(self):
        return True

class AgeLimitationPolicy(BuyingPolicy):
    def apply_policy(self, user, item):


