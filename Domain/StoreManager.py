from .User import User


# interface
class StoreManager(User):

    def __init__(self, username, password, age, country, appointer, permissions=None):
        super(StoreManager, self).__init__(username, password, age, country)
        self.permissions = permissions
        self.appointer = appointer
        if permissions is None:
            self.permissions = {'Edit': False, 'Remove': False, 'Add': False, 'Discounts': False}

