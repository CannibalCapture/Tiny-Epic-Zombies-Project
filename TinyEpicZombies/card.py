class Card:
    def __init__(self, player=-1, image="", type=""):
        self.player = player
        self.image = image
        self.type = type

class MeleeWeapon(Card):
    def __init__(self):
        pass

class BackpackItem(Card):
    def __init__(self):
        pass