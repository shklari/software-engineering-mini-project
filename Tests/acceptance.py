from django.test import TestCase
from Domain import SystemManager


def return_true():
    return True


def return_false():
    return False


class InitTestCase(TestCase):

    def setUp(self):

       # manager = SystemManager("mana", "123456")
