from Domain import User


# Interface
class StoreManager(User):

    def __init__(self, new_name, new_password, appointer=0):
        super().__init__(new_name, new_password)
        self.appointer = appointer
