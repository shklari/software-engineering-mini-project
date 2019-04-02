from unittest import TestCase
from Domain.System import System


class UnitTestSystem(TestCase):
    def setUp(self):
        self.system = System()


class TestInit(UnitTestSystem):
    def test_init_system(self):
        self.assertEqual(self.system.system_manager, 0)
        self.assertEqual(self.system.cur_user, 0)
        self.assertDictEqual(self.system.users, {})
        self.assertEqual(self.system.stores, [])
        self.assertEqual(self.system.init_system('shaioz', None), None)
        self.system.init_system('shaioz', 1234)
        self.assertEqual(self.system.system_manager.username, 'shaioz')
        self.assertGreater(len(self.system.users), 0)


class TestUser(UnitTestSystem):

    def test_sign_up(self):
        self.fail()

    def test_login(self):
        self.fail()

    def test_logout(self):
        self.fail()

    def test_remove_user(self):
        self.fail()


class TestStore(UnitTestSystem):
    def test_create_store(self):
        self.fail()
