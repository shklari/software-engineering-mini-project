from .Guest import Guest
from .BuyingPolicy import *


class User(Guest):
    creditDetails = {}

    def __init__(self, username, password):
        super(User, self).__init__()
        self.username = username
        self.password = password
        self.buying_policy = ImmediateBuyingPolicy()
        self.age
        self.country
