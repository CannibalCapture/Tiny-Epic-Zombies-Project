class Card:
    def __init__(self, player=-1):
        pass

class MeleeWeapon(Card):
    def __init__(self):
        self.type = "MELEE WEAPON"

class RangedWeapon(Card):
    def __init__(self):
        self.type = "RANGED WEAPON"

class BackpackItem(Card):
    def __init__(self):
        self.type = "BACKPACK ITEM"