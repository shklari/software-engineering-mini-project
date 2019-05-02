from unittest import TestCase
from Domain.System import System


class SystemIntegrationTests(TestCase):
    def setUp(self):
        self.system = System()
        self.system.init_system('shaioz', '1234')


class TestUserActions(SystemIntegrationTests):
    def test_good_signup_login(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12'))
        self.assertTrue(self.system.login('avokadosh', 'Aa12'))

    def test_bad_signup_login(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12'))
        self.assertFalse(self.system.login('avokadosh', 'aA12'), 'wrong password')
        self.assertFalse(self.system.login('facade', 'Aa12'), 'wrong username')

    def test_good_logout(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12'))
        self.assertTrue(self.system.login('avokadosh', 'Aa12'))
        self.assertTrue(self.system.logout())

    def test_bad_logout(self):
        self.assertFalse(self.system.logout(), 'no one is logged in')
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12'))
        self.assertTrue(self.system.login('avokadosh', 'Aa12'))
        self.assertTrue(self.system.logout())
        self.assertFalse(self.system.logout(), 'cannot log out twice')

    def test_good_remove_user(self):
        self.assertTrue(self.system.sign_up('ava bash', '666'))
        self.assertTrue('ava bash' in self.system.users)
        self.assertTrue(self.system.login('shaioz', '1234'))
        self.assertTrue(self.system.remove_user('ava bash'), 'removing ava from user list')
        self.assertFalse('ava bash' in self.system.users, 'ava is no longer a user')
        self.assertTrue(self.system.logout())

    def test_bad_remove_user(self):
        self.assertTrue(self.system.sign_up('ava bash', '666'))
        self.assertTrue(self.system.sign_up('avokadosh', '9876'))
        self.assertTrue(self.system.login('ava bash', '666'))
        self.assertFalse(self.system.remove_user('avokadosh'), 'ava is not system manager')
        self.assertTrue(self.system.logout())
        self.assertTrue(self.system.login('shaioz', '1234'))
        self.assertFalse(self.system.remove_user('shaioz'), 'system manager can not remove himself')
        self.assertFalse(self.system.remove_user('inbar'), 'user does not exist')
        self.assertTrue(self.system.remove_user('avokadosh'), 'removing a user from user list')
        self.assertFalse(self.system.remove_user('avokadosh'), 'user does not exist anymore')


class TestStoreAction(SystemIntegrationTests):
    def test_good_store_open(self):
        self.assertTrue(self.system.sign_up('ava bash', '666'))
        self.assertTrue(self.system.login('ava bash', '666'))
        self.assertEqual(len(self.system.stores), 0)
        self.assertTrue(self.system.create_store('avastore'))
        self.assertGreater(len(self.system.stores), 0)

    def test_bad_store_open(self):
        self.assertFalse(self.system.create_store('zara'), 'not logged in yet')
        self.assertEqual(len(self.system.stores), 0)
        self.assertTrue(self.system.sign_up('ava bash', '666'))
        self.assertTrue(self.system.login('ava bash', '666'))
        self.assertTrue(self.system.create_store('zara'))
        self.assertFalse(self.system.create_store('zara'), 'store name already exists')

    def test_good_add_owner_manager(self):
        self.assertTrue(self.system.sign_up('ava bash', '666'))
        self.assertTrue(self.system.sign_up('inbar', '9876'))
        self.assertTrue(self.system.sign_up('shklark', '6789'))
        inbar = self.system.get_user('inbar')
        itay = self.system.get_user('shklark')
        self.assertTrue(self.system.login('ava bash', '666'))
        self.assertTrue(self.system.create_store('avastore'))
        self.assertTrue(self.system.add_owner_to_store('avastore', 'inbar'))
        self.assertTrue(self.system.add_manager_to_store('avastore', 'shklark', 7))

