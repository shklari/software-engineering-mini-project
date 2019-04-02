

#interface
class StoreManager (object):

    def __init__(self, username, password, appointer, permissions = {'Edit': False, 'Remove': False, 'Add': False}):
        super(StoreManager, self).__init__(username, password)
        self.permissions = permissions
        self.appointer = appointer
        self.permissions = permissions

