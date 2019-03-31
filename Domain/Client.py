from Domain import User


# Interface
class ClientUser(User):

    def __init__(self, name, price, policy=0):
        self.name = name
        self.price = price
        self.policy = policy
