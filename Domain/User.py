from .Guest import Guest
from .BuyingPolicy import *


class User(Guest):
    creditDetails = {}

    def __init__(self, username, password, age, country):
        super(User, self).__init__()
        self.username = username
        self.password = password
        self.age = age
        self.country = country
        self.buying_policy = ImmediateBuyingPolicy()
