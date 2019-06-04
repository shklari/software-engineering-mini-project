from unittest import TestCase
from Domain.System import System


class SystemIntegrationTests(TestCase):
    def setUp(self):
        self.system = System()
        self.system.init_system('shaioz', '1234')


class TestUserActions(SystemIntegrationTests):
    def test_good_signup_login(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12').success)
        self.assertTrue(self.system.login('avokadosh', 'Aa12').success)

    def test_bad_signup_login(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12').success)
        self.assertFalse(self.system.login('avokadosh', 'aA12').success, 'wrong password')
        self.assertFalse(self.system.login('facade', 'Aa12').success, 'wrong username')

    def test_good_logout(self):
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12').success)
        self.assertTrue(self.system.login('avokadosh', 'Aa12').success)
        self.assertTrue(self.system.logout().success)

    def test_bad_logout(self):
        self.assertFalse(self.system.logout().success, 'no one is logged in')
        self.assertTrue(self.system.sign_up('avokadosh', 'Aa12').success)
        self.assertTrue(self.system.login('avokadosh', 'Aa12').success)
        self.assertTrue(self.system.logout().success)
        self.assertFalse(self.system.logout().success, 'cannot log out twice')

    def test_good_remove_user(self):
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue('ava bash' in self.system.users)
        self.assertTrue(self.system.login('shaioz', '1234').success)
        self.assertTrue(self.system.remove_user('ava bash').success, 'removing ava from user list')
        self.assertFalse('ava bash' in self.system.users, 'ava is no longer a user')
        self.assertTrue(self.system.logout().success)

    def test_bad_remove_user(self):
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue(self.system.sign_up('avokadosh', '9876').success)
        self.assertTrue(self.system.login('ava bash', '666').success)
        self.assertFalse(self.system.remove_user('avokadosh').success, 'ava is not system manager')
        self.assertTrue(self.system.logout().success)
        self.assertTrue(self.system.login('shaioz', '1234').success)
        self.assertFalse(self.system.remove_user('shaioz').success, 'system manager can not remove himself')
        self.assertFalse(self.system.remove_user('inbar').success, 'user does not exist')
        self.assertTrue(self.system.remove_user('avokadosh').success, 'removing a user from user list')
        self.assertFalse(self.system.remove_user('avokadosh').success, 'user does not exist anymore')


class TestStoreAction(SystemIntegrationTests):
    def test_good_store_open(self):
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue(self.system.login('ava bash', '666').success)
        self.assertEqual(len(self.system.stores), 0)
        self.assertTrue(self.system.create_store('avastore').success)
        self.assertGreater(len(self.system.stores), 0)

    def test_bad_store_open(self):
        self.assertFalse(self.system.create_store('zara').success, 'not logged in yet')
        self.assertEqual(len(self.system.stores), 0)
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue(self.system.login('ava bash', '666').success)
        self.assertTrue(self.system.create_store('zara').success)
        self.assertFalse(self.system.create_store('zara').success, 'store name already exists')

    def test_good_add_owner_manager(self):
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue(self.system.sign_up('inbar', '9876').success)
        self.assertTrue(self.system.sign_up('shklark', '6789').success)
        self.assertTrue(self.system.login('ava bash', '666').success)
        self.assertTrue(self.system.create_store('avastore').success)
        self.assertTrue(self.system.add_owner_to_store('avastore', 'inbar').success)
        self.assertTrue(self.system.add_manager_to_store('avastore', 'shklark', 7).success)

    def test_good_get_total_system_inventory(self):
        self.assertTrue(self.system.sign_up('ava bash', '666').success)
        self.assertTrue(self.system.login('ava bash', '666').success)
        ava = self.system.get_cur_user()
        avaStore = self.system.create_store('avaStore')
        self.assertTrue(avaStore.success)
        gun = {'name': "glock", 'price': 5000, 'category': "weapon"}
        axe = {'name': "axe", 'price': 200, 'category': "weapon"}
        bamba = {'name': "bamba", 'price': 5, 'category': "snak"}
        self.assertTrue((avaStore.value.add_item_to_inventory(ava, gun, 14)).success)
        self.assertTrue((avaStore.value.add_item_to_inventory(ava, axe, 502)).success)
        self.assertTrue((avaStore.value.add_item_to_inventory(ava, bamba, 80)).success)
        self.system.logout()
        self.assertTrue((self.system.sign_up('inbar', '9876')).success)
        self.assertTrue((self.system.login("inbar", '9876')).success)
        inbar = self.system.get_cur_user()
        inbarStore = self.system.create_store('inbarStore')
        self.assertTrue(inbarStore.success)
        bread = {'name': "bread", 'price': 4, 'category': "food"}
        hala = {'name': "hala", 'price': 8, 'category': "food"}
        self.assertTrue((inbarStore.value.add_item_to_inventory(inbar, bread, 100)).success)
        self.assertTrue((inbarStore.value.add_item_to_inventory(inbar, hala, 150)).success)
        inv = self.system.get_total_system_inventory()
        self.assertTrue(len(inv.value) == 5)
        print("the inventory is:\n")
        print(inv.value)
