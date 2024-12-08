class Card:
    def __init__(self, player=-1):
        pass

    def serialize(self):
        return {}

class MeleeWeapon(Card):
    def __init__(self):
        self.type = "MELEE WEAPON"

    def serialize(self):
        return { "type": self.type }

    def deserialize(dict):
        return MeleeWeapon()

class RangedWeapon(Card):
    def __init__(self):
        self.type = "RANGED WEAPON"

    def serialize(self):
        return { "type": self.type }
    
    def deserialize(dict):
        return RangedWeapon()

class BackpackItem(Card):
    def __init__(self):
        self.type = "BACKPACK ITEM"
    
    def serialize(self):
        return { "type": self.type }