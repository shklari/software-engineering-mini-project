from unittest import TestCase
from Domain.System import System


class UnitTestSystem(TestCase):
    def setUp(self):
        self.system = System()


class TestInit(UnitTestSystem):
    def test_init_system(self):
        self.assertEqual(self.system.system_manager, None)
        self.assertEqual(self.system.cur_user, None)
        self.assertDictEqual(self.system.users, {})
        self.assertEqual(self.system.stores, [])
        self.assertEqual(self.system.init_system('shaioz', None, 21, "").success, False)  # empty password isn't valid.
        self.system.init_system('shaioz', '1234', 21, "")
        self.assertEqual(self.system.system_manager.username, 'shaioz')
        self.assertGreater(len(self.system.users), 0)


class TestUser(UnitTestSystem):

    def test_sign_up(self):
        self.system.init_system('shaioz', '1234', 21, "")
        self.assertTrue(self.system.sign_up('ava bash', '666', 21, "").success)
        self.assertTrue(self.system.sign_up('shkalrk', '1234', 21, "").success)
        self.assertFalse(self.system.sign_up('ava bash', '666', 21, "").success, 'user already exist')
        self.assertFalse(self.system.sign_up('avokadosh', '', 21, "").success, 'invalid password')
        self.assertFalse(self.system.sign_up('', '4444', 21 , "").success, 'invalid username')
        self.assertFalse(self.system.cur_user.logged_in, 'no user is logged in')

    def test_login(self):
        self.system.init_system('shaioz', '1234', 21, "")
        self.assertFalse(self.system.cur_user.logged_in, 'no one is signed in')
        self.assertFalse(self.system.login('avokadosh', '9876').success, 'user not signed up')
        self.system.sign_up('avokadosh', '9876', 21, "")
        self.assertFalse(self.system.login('avokadosh', '9877').success, 'wrong password')
        self.assertTrue(self.system.login('avokadosh', '9876').success)
        self.assertTrue(self.system.cur_user.logged_in)
        self.assertFalse(self.system.login('avokadosh', '9876').success, 'already logged in')

    def test_logout(self):
        self.system.init_system('shaioz', '1234', 21, "")
        self.assertFalse(self.system.logout().success, 'no one is signed in')
        self.system.login('shaioz', '1234')
        self.assertTrue(self.system.logout().success)
        self.assertFalse(self.system.cur_user.logged_in, 'user in now logged out')

    def test_remove_user(self):
        self.system.init_system('shaioz', '1234', 21, "")
        self.system.sign_up('ava bash', '666', 21, "")
        self.system.sign_up('avokadosh', '9876', 21, "")
        self.system.login('ava bash', '666')
        self.assertFalse(self.system.remove_user('avokadosh').success, 'ava is not system manager')
        self.system.create_store('zara')
        self.system.create_store('pnb')
        self.system.logout()
        self.system.login('shaioz', '1234')
        self.assertFalse(self.system.remove_user('shaioz').success, 'system manager can not remove himself')
        self.assertFalse(self.system.remove_user('inbar').success, 'user does not exist')
        self.assertTrue(self.system.remove_user('avokadosh').success, 'removing a user from user list')
        self.assertFalse(self.system.remove_user('avokadosh').success, 'user does not exist anymore')
        found_avas_store = False
        for store in self.system.stores:
            for owner in store.storeOwners:
                if owner.username == 'ava bash':
                    found_avas_store = True
        self.assertTrue(found_avas_store, 'found avas stores')
        found_avas_store = False
        self.system.remove_user('ava bash')
        for store in self.system.stores:
            for owner in store.storeOwners:
                if owner.username == 'ava bash':
                    found_avas_store = True
        self.assertFalse(found_avas_store, 'ava bash was removed so all of her stores are removed')


class TestStore(UnitTestSystem):
    def test_create_store(self):
        self.system.init_system('shaioz', '1234', 21, "")
        self.assertFalse(self.system.create_store('zara').success, 'not logged in yet')
        self.assertEqual(len(self.system.stores), 0)
        self.system.login('shaioz', '1234')
        self.assertTrue(self.system.create_store('zara').success)
        self.assertFalse(self.system.create_store('zara').success, 'store name already exists')
        self.assertEqual(len(self.system.stores), 1)
        self.assertEqual(self.system.stores[0].name, 'zara')



