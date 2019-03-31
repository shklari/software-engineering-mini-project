import unittest
from Service.service import SystemInterface


class TestStore(unittest.TestCase):

    service = SystemInterface()

    def setUp(self):
        manager = {'name': 'mana', 'password': '123456'}
        manager["name"]

    def addToCartTest(self):
        service.add_to_cart()
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
