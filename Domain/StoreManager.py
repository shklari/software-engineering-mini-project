

#interface
class StoreManager (object):

    def __init__(self, username, password, appointer):
        super(StoreManager, self).__init__(username, password)
        self.permissions = {'Edit': False, 'Remove': False, 'Add': False}
        self.appointer = appointer

    def set_permissions(self, new_permissions):
        self.permissions = new_permissions

