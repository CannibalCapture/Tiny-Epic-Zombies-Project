from .card import Card

class MeleeWeapon(Card):
    def __init__(self):
        self.type = "MELEE WEAPON"

    def serialize(self):
        return { "type": self.type }

    def deserialize(dict):
        return MeleeWeapon()