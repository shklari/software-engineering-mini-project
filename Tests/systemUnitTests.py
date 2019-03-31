import unittest

from Service.service import SystemInterface, CollectingSystem, SupplyingSystem, IntegritySystem


class AllTestCase(unittest.TestCase):

    system = SystemInterface()
    def setUp(self):

        self.manager = {"backet": 0, "name": "man", "password": "123456"}
        self.collecting = CollectingSystem()
        self.supplying = SupplyingSystem()
        self.integrity = IntegritySystem()

    def test_bad_systems(self):
        for(i in range(0, 1)):
            for(j in range(0, 1)):
                for(k in range(0, 1)):
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
