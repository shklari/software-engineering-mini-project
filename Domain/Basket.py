from .CollectingSystem import CollectingSystem


class Basket:
    def __init__(self):
        self.carts = []
        self.collectingSystem = CollectingSystem()