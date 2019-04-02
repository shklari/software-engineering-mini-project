

#interface
class StoreManager (object):

    def __init__(self, username, password, appointer, permissions):
        super(StoreManager, self).__init__(username, password)
        self.permissions = {'Edit': False, 'Remove': False, 'Add': False}
        self.appointer = appointer
        self.permissions = permissions

