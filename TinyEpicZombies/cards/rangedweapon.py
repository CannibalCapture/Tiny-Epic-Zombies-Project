from .card import Card

class RangedWeapon(Card):
    def __init__(self):
        self.type = "RANGED WEAPON"

    def serialize(self):
        return { "type": self.type }
    
    def deserialize(dict):
        return RangedWeapon()