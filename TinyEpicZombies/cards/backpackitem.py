from .card import Card

class BackpackItem(Card):
    def __init__(self):
        self.type = "BACKPACK ITEM"
    
    def serialize(self):
        return { "type": self.type }