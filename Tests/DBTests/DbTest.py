from mockupdb import go, MockupDB
import unittest
from DataAccess.mongoDB import DB
from Domain.Item import Item
from Domain.Store import Store
from Domain.User import User


class DbTest(unittest.TestCase):

    def setUp(self):

        self.database = DB()
        self.user1 = User("sharon", "1234", 27, "israel")
        self.user2 = User("sharon1", "123", 21, "USA")
        self.user3 = User("sharon3", "111", 24, "UK")
        self.user4 = User("sharon4", "000", 25, "canada")
        self. user5 = User("sharon5", "222", 28, "china")
        self.item = Item("thisIsItem", 7, "sport", "sharon_inc")
        self.item1 = Item("anotherItem", 5, "music", "sharon_inc")
        self.store = Store("sharon_inc", self.user1, 0)

    def test_add(self):
        self.database.add_user(self.user1)
        self.assertEqual(self.database.get_user(self.user1.username).username, self.user1.username)
        self.assertFalse(self.database.get_user(self.user2.username) == self.user2.username)
        self.database.add_store(self.store, self.user1.username)
        self.assertEqual(self.database.get_store(self.store.name).name, self.store.name)
        self.database.add_cart(self.user1.username, self.store.name, self.item.name, 2, self.item.price, self.item.category)
        self.database.add_user(self.user2)
        self.database.add_user(self.user3)
        self.database.add_store_owner(self.store.name, self.user2.username, self.user1.username)
        self.database.add_store_manager(self.store.name, self.user3.username, self.user1.username, "true", "false", "false", "false")

    def test_remove(self):
        self.database.remove_user(self.user1.username)
        self.assertFalse(self.database.get_user(self.user1.username) == self.user1.username)
        self.database.remove_store(self.store.name)
        self.assertFalse(self.database.get_store(self.store.name) == self.store.name)


if __name__ == '__main__':
    unittest.main()
