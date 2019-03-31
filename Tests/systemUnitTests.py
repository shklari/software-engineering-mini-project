import unittest
from django.test import TestCase
from Service.service import SystemInterface


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


class IntegritySystem(object):

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


class AllTestCase(TestCase):

    def setUp(self) -> None:
        self.system = SystemInterface()
        self.manager = {"bascket": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.integrity = IntegritySystem()

    def test_init(self):
        for i in range(0, 1):
            for j in range(0, 1):
                for k in range(0, 1):
                    self.assertEqual((i == 1 and j == 1 and k == 1), self.system.init(self.manager, self.collecting, self.supplying, self.integrity))
                    self.collecting.switch()
                self.supplying.switch()
            self.integrity.switch()


class TestStringMethods(unittest.TestCase):

    service = SystemInterface()

    def setUp(self):
        manager = {'name': 'mana', 'password': '123456'}
        manager["name"]

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
