import unittest

from Domain.BuyingPolicy import *


class FailImmediatePC(BuyingPolicy):

    def apply_policy(self):
        return False

    def is_composite(self):
        return False


class TestImmediateBP(unittest.TestCase):

    policy = ImmediateBuyingPolicy()

    def test_immediate_policy(self):
        self.assertTrue(self.policy.apply_policy())

    def test_is_comp(self):
        self.assertFalse(self.policy.is_composite())


class TestCompositeBP(unittest.TestCase):

    def setUp(self) -> None:
        self.comp = CompositeBuyingPolicy()

    def test_empty_composite(self):
        self.assertTrue(self.comp.apply_policy())

    def test_is_comp(self):
        self.assertTrue(self.comp.apply_policy())

    def test_add_policy(self):
        policy = ImmediateBuyingPolicy()
        self.comp.add_policy(policy)
        self.assertTrue(policy in self.comp.policies)

    def test_apply_policy(self):
        self.assertTrue(self.comp.apply_policy())
        self.comp.add_policy(ImmediateBuyingPolicy())
        self.assertTrue(self.comp.apply_policy())
        comp2 = CompositeBuyingPolicy()
        comp2.add_policy(self.comp)
        self.assertTrue(comp2.apply_policy())
        negative_pol = FailImmediatePC()
        self.comp.add_policy(negative_pol)
        self.assertFalse(self.comp.apply_policy())
        self.assertFalse(comp2.apply_policy())
        self.comp.remove_policy(negative_pol)
        comp2.add_policy(negative_pol)
        self.assertTrue(self.comp.apply_policy())
        self.assertFalse(comp2.apply_policy())

