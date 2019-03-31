

# Interface
class Item:

    def __init__(self, name, price, category, rank):
        self.name = name
        self.price = price
        self.category = category
        self.rank = rank

    def set_policy(self, new_policy): pass

    # 4.1.3
    def set_price(self, new_price): pass